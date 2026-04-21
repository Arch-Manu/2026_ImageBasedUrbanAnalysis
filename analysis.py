from agents import *
import json
import re
from typing import Callable


def _extract_json_object(text: str, start_idx: int) -> str | None:
    """Return balanced JSON object substring starting at start_idx, or None."""
    if start_idx >= len(text) or text[start_idx] != "{":
        return None
    depth = 0
    in_string = False
    escape = False
    for i in range(start_idx, len(text)):
        c = text[i]
        if in_string:
            if escape:
                escape = False
            elif c == "\\":
                escape = True
            elif c == '"':
                in_string = False
            continue
        if c == '"':
            in_string = True
        elif c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return text[start_idx : i + 1]
    return None


def parse_urban_dna(synthesis_text: str) -> dict | None:
    """
    Parse the JSON object following the 'URBAN DNA' heading in synthesis output.
    Returns None if no valid JSON block is found.
    """
    if not synthesis_text:
        return None

    def _loads_urban_block(after: str) -> dict | None:
        chunk = after.lstrip()
        if chunk.startswith("```"):
            nl = chunk.find("\n")
            if nl != -1:
                chunk = chunk[nl + 1 :]
            fe = chunk.rfind("```")
            if fe != -1:
                chunk = chunk[:fe].strip()
        brace = chunk.find("{")
        if brace == -1:
            return None
        raw = _extract_json_object(chunk, brace)
        if raw is None:
            return None
        try:
            data = json.loads(raw)
            return data if isinstance(data, dict) else None
        except json.JSONDecodeError:
            return None

    m = re.search(r"URBAN\s+DNA\s*", synthesis_text, re.IGNORECASE)
    if m:
        parsed = _loads_urban_block(synthesis_text[m.end() :])
        if parsed is not None:
            return parsed
    return None


def merge_urban_from_vision(
    urban_dna: dict | None,
    vision_parsed: dict | None,
) -> dict | None:
    """
    Fill gaps in synthesis Urban DNA using root-level Vision JSON (aggregate scores, etc.).
    Ensures metrics/charts still populate when synthesis JSON parsing is incomplete.
    """
    out: dict = {}
    if isinstance(urban_dna, dict):
        out.update(urban_dna)
    if not isinstance(vision_parsed, dict):
        return urban_dna if urban_dna else (out or None)

    vp = vision_parsed
    has_agg = any(
        k in out for k in ("Aggregate Scores", "aggregate_scores")
    )
    if not has_agg:
        agg = vp.get("aggregate_scores")
        if isinstance(agg, dict) and agg:
            out["Aggregate Scores"] = agg

    if not (out.get("Insights") or out.get("insights")):
        street = vp.get("street")
        if isinstance(street, dict):
            bits = []
            if street.get("name"):
                bits.append(f"Street: {street['name']}.")
            if street.get("overall_liveability_mean") is not None:
                bits.append(
                    f"Overall liveability (vision): {street['overall_liveability_mean']}."
                )
            if bits:
                out.setdefault("Insights", " ".join(bits))

    return out if out else None


def parse_vision_output(vision_text: str | dict | None) -> dict | None:
    """
    Parse the Vision Agent JSON from ``output_text`` (may be fenced or double-encoded).
    Expected shape includes a ``photos`` list with per-image ``urban_analysis``.
    """
    if vision_text is None:
        return None
    if isinstance(vision_text, dict):
        return vision_text
    if not isinstance(vision_text, str):
        return None
    text = vision_text.strip()
    if not text:
        return None
    if text.startswith("```"):
        first_nl = text.find("\n")
        if first_nl != -1:
            text = text[first_nl + 1 :]
        fence = text.rfind("```")
        if fence != -1:
            text = text[:fence].strip()
    for _ in range(5):
        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            break
        if isinstance(data, dict):
            return data
        if isinstance(data, str):
            text = data.strip()
            continue
        return None
    brace = text.find("{")
    if brace != -1:
        raw = _extract_json_object(text, brace)
        if raw:
            try:
                data = json.loads(raw)
                if isinstance(data, dict):
                    return data
            except json.JSONDecodeError:
                pass
    return None


def get_vision_photo_detail(
    parsed: dict | None,
    index: int,
    upload_filename: str | None = None,
) -> dict | None:
    """
    Return per-upload vision fields for the selected image.

    Uses ``upload_filename`` (when provided) to match ``photos[].filename``;
    otherwise falls back to list order ``index`` or ``photo_index``.

    Returns keys: tags, narrative, verdict, description, overall_score (optional).
    """
    if not parsed or not isinstance(parsed, dict):
        return None
    photos = parsed.get("photos")
    if not isinstance(photos, list) or not photos:
        return None
    photo = None
    if upload_filename:
        want = Path(upload_filename).name.lower()
        for p in photos:
            if not isinstance(p, dict):
                continue
            fn = p.get("filename") or ""
            if fn and Path(fn).name.lower() == want:
                photo = p
                break
    if photo is None and 0 <= index < len(photos):
        photo = photos[index]
    if photo is None:
        for p in photos:
            if isinstance(p, dict) and p.get("photo_index") == index:
                photo = p
                break
    if not isinstance(photo, dict):
        return None
    ua = photo.get("urban_analysis")
    if not isinstance(ua, dict):
        ua = {}
    raw_tags = ua.get("detected_elements")
    if raw_tags is None:
        raw_tags = ua.get("Detected elements")
    tags = list(raw_tags) if isinstance(raw_tags, list) else []
    narrative = (ua.get("narrative") or "").strip()
    verdict = (ua.get("verdict") or "").strip()
    description = narrative if narrative else verdict
    return {
        "tags": tags,
        "narrative": narrative,
        "verdict": verdict,
        "description": description,
        "overall_score": ua.get("overall_score"),
    }


def run_analysis(
    image_paths: list,
    *,
    on_progress: Callable[[str, float], None] | None = None,
) -> dict:
    """
    Run the full vision → pattern → insights → place → synthesis pipeline.

    Parameters
    ----------
    image_paths : list
        List of filesystem paths to image files (strings or Path-like).
    on_progress : callable, optional
        ``on_progress(message, fraction)`` where ``fraction`` is in ``[0, 1]``
        and advances after each agent step (for UI progress bars).

    Returns
    -------
    dict with keys:
        vision_response, vision_text, pattern, insights, place,
        synthesis_text, urban_dna (parsed dict or None)
    """
    paths = [str(p) for p in image_paths]
    if not paths:
        raise ValueError("run_analysis requires at least one image path")

    if on_progress:
        progress_text = "Analysing images with Vision Agent…"
        on_progress(progress_text, 0.0)
    vision_data = vision_agent(paths)
    vision_text = vision_data.output_text

    if on_progress:
        progress_text = progress_text + "                                                      Identifying patterns with Pattern Agent…"
        on_progress(progress_text, 1 / 5)
    pattern_data = pattern_agent(vision_data)

    if on_progress:
        progress_text = progress_text + "                                                      Analysing street insights with Insights Agent…"
        on_progress(progress_text, 2 / 5)
    insights_data = insights_agent(vision_data)

    if on_progress:
        progress_text = progress_text + "                                                      Extracting place information with Place Agent…"
        on_progress(progress_text, 3 / 5)
    place_data = place_agent()

    if on_progress:
        progress_text = progress_text + "                                                      Synthesising urban intelligence…"
        on_progress(progress_text, 4 / 5)
    final = synthesis_agent(
        {
            "vision": vision_data,
            "place": place_data,
            "pattern": pattern_data,
            "insights": insights_data,
        }
    )
    synthesis_text = final.output_text
    vision_parsed = parse_vision_output(vision_text)
    urban_dna = parse_urban_dna(synthesis_text)
    urban_dna = merge_urban_from_vision(urban_dna, vision_parsed)

    if on_progress:
        progress_text = "Analysis Complete!"
        on_progress(progress_text, 1.0)

    return {
        "vision_response": vision_data,
        "vision_text": vision_text,
        "vision_parsed": vision_parsed,
        "pattern": pattern_data,
        "insights": insights_data,
        "place": place_data,
        "synthesis_text": synthesis_text,
        "urban_dna": urban_dna,
    }


def dna_pick(dna: dict | None, *keys: str):
    """Return the first present key's value from an Urban DNA dict (model output may vary)."""
    if not dna:
        return None
    for k in keys:
        if k in dna:
            return dna[k]
    return None


if __name__ == "__main__":

    ROOT_DIR = Path(__file__).parent
    IMG_DIR = ROOT_DIR / "images"

    images = []
    for file in os.listdir(IMG_DIR):
        if file.endswith(
            (".JPG", ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp")
        ):
            images.append(os.path.join(IMG_DIR, file))

    if not images:
        print(f"No images found in {IMG_DIR}")
        raise SystemExit(1)

    print("\nRunning full analysis pipeline…\n")
    result = run_analysis(images)

    print("VISION DATA:\n", result["vision_response"])
    print("\nPATTERN DATA:\n", result["pattern"])
    print("\nINSIGHTS DATA:\n", result["insights"])
    print("\nPLACE DATA:\n", result["place"])
    print("\nSYNTHESIS:\n", result["synthesis_text"])

    if result["urban_dna"] is not None:
        print("\n--- Parsed URBAN DNA (JSON) ---\n")
        print(json.dumps(result["urban_dna"], indent=2))
