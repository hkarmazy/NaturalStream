# Stream Analysis App - Enhanced Features Update

## Summary of Changes

The Streamlit web app has been significantly enhanced with advanced features for custom item labeling and improved data visualization.

## New Features Added

### 1. ✨ Custom Options (The Options) Configuration

**Location**: Left sidebar, under "🏷️ The Options (Optional)"

**What It Does**:
- Allows users to specify custom string labels for items in the stream
- Optional feature - not required to run the analysis
- Works with the existing 4 episode parameters

**How to Use**:
1. Click "Configure Options" to expand the section
2. Enter labels for each item (e.g., "Product A", "Action 1", "State X")
3. Leave fields empty to use default numeric values (1, 2, 3, ...)
4. Choose mapping order: "Ranked" or "Random"

**Order Types**:
- **Ranked** (Sequential): First label → First state, Second label → Second state, etc.
- **Random** (Default): Labels are randomly assigned to states (uses fixed seed 42 for reproducibility)

### 2. 🏷️ Dynamic Label Display Based on Order

- If "Ranked" is selected: Shows how labels map sequentially
- If "Random" is selected: Shows random assignment preview
- Visual indicator showing number of custom labels provided

### 3. 📊 Enhanced Network Graph Visualization

**Node Improvements**:
- **Larger Nodes**: Increased size from 400 to 800 for better visibility
- **Smart Labels**: 
  - If custom options provided: Shows the custom labels
  - If default: Shows numeric rank values
- **Better Positioning**: Text labels centered on nodes

**Visualization Example**:
```
Network with Custom Labels:        Network with Default:
    [Apple]                            [1]
    /  \  \                           / \ \
  [Banana]                          [2]
    |                                  |
  [Orange]                           [3]
```

### 4. 📥 Enhanced Downloads Tab

**Three Download Options Now Available**:

1. **Frequency Table (CSV)**
   - Contains frequency analysis data
   - State column shows custom labels if provided
   - Includes: State, Frequency, Rank, Proportion, Cumulative

2. **Stream Data (CSV)** 
   - Raw stream data as generated
   - Numeric values (1 to Episode Options)
   - Original format for technical analysis

3. **Stream by Ranked Order (NEW!)**
   - Shows selected items for each time step
   - Uses custom labels if provided
   - Includes live preview of first 5 rows
   - Comma-separated format for easy importing

**Example Output**:
```
Time Step 1: Apple, Banana
Time Step 2: Banana, Orange
Time Step 3: Apple, Apple
...
```

### 5. 📋 Updated Frequency Table Display

**Changes**:
- Automatically applies custom labels to State column
- Maintains all other columns unchanged
- Clean, readable format with proper headers

**Example**:
| State   | Freq | rank | prop   | cumulative |
|---------|------|------|--------|------------|
| Apple   | 45   | 1    | 0.375  | 0.375      |
| Banana  | 30   | 2    | 0.250  | 0.625      |
| Orange  | 25   | 3    | 0.208  | 0.833      |

## Technical Implementation Details

### Label Mapping Algorithm

```python
# Ranked Order Mapping
unique_states = sorted(FTable['State'].unique())
for i, state in enumerate(unique_states):
    state_to_option_mapping[state] = provided_options[i]

# Random Order Mapping  
np.random.seed(42)
shuffled_options = np.random.permutation(provided_options)
for i, state in enumerate(unique_states):
    state_to_option_mapping[state] = shuffled_options[i]
```

### Node Label Display
```python
if option_labels and has_custom_options:
    node_labels[node] = option_labels[node]
else:
    node_labels[node] = str(node)  # Numeric rank
```

### Stream Export with Labels
- Reads the mapping from state → option
- Replaces numeric values with labels in output
- Preserves order of items selected at each time step

## Usage Examples

### Example 1: Analyzing Product Preferences

**Setup**:
- Episode Options: 5
- Options Order: Ranked
- Custom Labels: ["Laptop", "Phone", "Tablet", "Monitor", "Keyboard"]

**Result**:
- State 1 → Laptop
- State 2 → Phone
- State 3 → Tablet
- Network graph shows product names on nodes
- Downloads include product preferences

### Example 2: Event Sequence Analysis

**Setup**:
- Episode Options: 4
- Options Order: Random
- Custom Labels: ["login", "click", "submit", "logout"]

**Result**:
- Labels randomly assigned to events
- Frequency table shows which event is most common
- Stream downloads labeled by event type
- Network shows event transitions

### Example 3: Default Numeric Analysis (No Custom Labels)

**Setup**:
- Just set Episode Options to desired value
- Leave "The Options" section empty
- No custom configuration needed

**Result**:
- All displays use numeric values 1, 2, 3, ...
- Works exactly as before
- No functional changes

## File Structure

```
Stream Analysis App/
├── streamlit_app.py              # Main app (UPDATED)
├── PlotsPart2.py                 # Reference script
├── THE_OPTIONS_GUIDE.md           # Detailed feature guide (NEW)
├── DEPLOYMENT_GUIDE.md            # GitHub deployment instructions
├── README_WEBAPP.md               # GitHub documentation
├── requirements.txt               # Dependencies
├── .streamlit/
│   └── config.toml               # Streamlit config
└── [Module files]
    ├── ModelTimeSeries.py
    ├── Ranking.py
    ├── clustering_coef_wu.py
    └── PowerLawFit.py
```

## Running the Updated App

### Locally
```bash
cd "/Users/hadar/Dropbox/Python Folder"
streamlit run streamlit_app.py
```

### On Streamlit Cloud
No changes needed - just push to GitHub and redeploy. Streamlit Cloud will use the updated app automatically.

## Backward Compatibility

✓ **Fully backward compatible**
- All existing workflows still work
- The Options section is optional
- Default behavior unchanged when not using custom labels
- Session state properly manages both old and new features

## Browser Compatibility

Works with all modern browsers:
- Chrome/Chromium ✓
- Firefox ✓
- Safari ✓
- Edge ✓

## Performance Considerations

- **No performance impact** when The Options are not used
- Custom label processing is minimal
- Network graph rendering unchanged (same size as before update)
- String handling is efficient

## Troubleshooting

### Labels Not Appearing in Network Graph
- Ensure "Generate Analysis" button was clicked after entering labels
- Check that labels aren't empty strings
- Try clearing browser cache

### Stream Download Shows Numbers Instead of Labels
- Confirm labels were entered in the Configuration section
- Verify "Generate Analysis" was clicked
- Check that labels weren't accidentally cleared

### Random Order Different Than Expected
- This is normal with seed=42 - same seed produces same randomization
- To change randomization, modify seed in code (line ~155)

## Future Enhancement Possibilities

- [ ] Import/export label configurations
- [ ] Batch analysis with multiple label sets
- [ ] Color-coding for label categories
- [ ] Drag-and-drop label reordering
- [ ] Label validation and suggestions
- [ ] A/B comparison between ranked vs random
- [ ] Label history/favorites

## Support & Feedback

For issues or feature requests, refer to THE_OPTIONS_GUIDE.md for detailed documentation.

---

**Version**: 2.0  
**Last Updated**: January 21, 2026  
**Backward Compatible**: Yes  
**Breaking Changes**: None
