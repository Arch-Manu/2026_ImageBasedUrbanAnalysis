# 🏙️ AI Urban Image Analyzer - Streamlit UI

A clean, efficient prototype UI that matches the React wireframe design, running on Streamlit.

## 🚀 Quick Start (One Command!)

```bash
streamlit run streamlit_app.py
```

Opens at: `http://localhost:8501` ⚡

## ✨ Design Features

- **Unified Interface**: Image upload + live metrics in one view
- **Professional Layout**: Matches React wireframe design
- **Real-time Visualization**: Charts, progress bars, and metric cards
- **Image Grid**: 3×4 thumbnail display
- **Urban Analytics**:
  - Material Distribution chart
  - Use Distribution pie chart
  - Height Ranges analysis
  - Urban DNA metrics
- **Image Details**: Tags, confidence scores, and descriptions
- **Clusters & Outliers**: Visual differentiation for analysis results

## 🎯 How to Use

1. **Upload Images** - Click "📤 Upload Images" and select multiple urban photos
2. **View Metrics** - See key metrics (Avg Height, Active Frontage, Dominant Use, Material)
3. **Analyze Visually** - Charts show Material Distribution, Use Distribution, Height Ranges
4. **Urban DNA** - Progress bars for Height, Activity, and Density
5. **Image Details** - Select an image to view tags, confidence scores, and description
6. **Clusters** - View groupings and outliers at the bottom

## 📦 Integration with Your Code

The Streamlit app integrates with:

- `analysis.py` - Your analysis pipeline
- `agents.py` - Your vision and context agents
- `synthetic_input.JSON` - Test data

## 🔧 Direct Python Integration

No separate backend needed. The app directly imports and runs your Python functions:

```python
from analysis import run_analysis, synthesis_agent
```

## 📋 Requirements

```bash
# Already installed
pip install streamlit
```

## 📁 Project Structure

```
2026_ImageBasedUrbanAnalysis/
├── streamlit_app.py              # Main UI (this is your interface!)
├── analysis.py                   # Analysis pipeline
├── agents.py                     # Vision + Context agents
├── synthetic_input.JSON          # Test data
├── STREAMLIT_QUICK_START.md      # This guide
└── README.md
```

## 💡 Key Customizations You Can Make

Edit `streamlit_app.py` to:

- **Change colors**: Modify CSS in the `st.markdown()` sections
- **Add more metrics**: Add to the `metrics` list
- **Change chart types**: Replace `st.bar_chart()` with `st.line_chart()`, etc.
- **Adjust layout**: Modify `st.columns()` ratios
- **Add filtering**: Add dropdown filters above the image grid
- **Connect real analysis**: Call `run_analysis()` when the button is clicked

## 🚨 Troubleshooting

**App won't start?**

```bash
cd /Users/smthspce/CodeRepos/00_GithubRepos/2026_ImageBasedUrbanAnalysis
streamlit run streamlit_app.py
```

**Import errors?**

- Make sure you're in the repo root directory
- Check that `analysis.py` and `agents.py` don't have syntax errors

**OpenAI API errors?**

- Ensure `.env` file has `OPENAI_API_KEY` set
- The UI will still display, but agent functions may fail

## 🎨 UI Architecture

The Streamlit app uses:

- **Custom CSS**: For metric cards and styling
- **Columns**: 5-7 split for image set and analysis
- **Progress bars**: For Urban DNA metrics
- **Charts**: Material, Use, and Height distributions
- **HTML embeds**: For custom-styled clusters and outliers

## 📊 Next Steps

- **Add real analysis**: Connect the "Run Analysis" button to `run_analysis()`
- **Add filters**: Cluster, Use, Confidence filters work with your data
- **Add export**: Download results as CSV or JSON
- **Add history**: Store and display previous analyses
- **Add caching**: Use `@st.cache_data` for faster re-runs

---

**UI Design**: Matches React wireframe  
**Backend**: Direct Python integration  
**Setup Time**: ~30 seconds  
**Perfect for**: Hackathons, rapid prototyping, demos

🎉 **Happy analyzing!**
