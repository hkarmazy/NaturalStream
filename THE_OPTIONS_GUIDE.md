# Stream Analysis Tool - Advanced Features Guide

## New Feature: The Options

The "The Options" feature allows you to assign custom labels to items in your stream analysis, making the results more interpretable and meaningful.

## How to Use The Options

### Step 1: Expand the Options Section
In the left sidebar, under "🏷️ The Options (Optional)", click "Configure Options" to expand the section.

### Step 2: Enter Custom Labels (Optional)
- You'll see input fields for each option (matching your "Episode Options" value)
- Enter a label for each option (e.g., "Product A", "Apple", "Type-1")
- Leave empty to use default numeric values (1, 2, 3, etc.)

### Step 3: Choose the Order Type
At the bottom of the Options section, you have two choices:

#### Ranked Order (Sequential Mapping)
- **What it does**: Maps your labels to states in sequential order
- **Example**: If your Episode Options = 3 and you enter ["Apple", "Banana", "Cherry"]
  - State 1 → "Apple"
  - State 2 → "Banana"  
  - State 3 → "Cherry"
- **When to use**: You want states to correspond to your labels in the exact order you provided

#### Random Order (Default)
- **What it does**: Randomly assigns your labels to states
- **Reproducibility**: Uses a fixed seed (42) for consistent results across runs
- **When to use**: You want a random distribution of your labels, or you don't care about state-to-label correspondence

## What Gets Affected by The Options

### 1. Frequency Table (Tab: Frequency Table)
- The "State" column displays your custom labels instead of numeric values
- All other columns (Freq, rank, prop, cumulative) remain the same

### 2. Network Graph (Tab: Main Analysis Plots)
- Node labels show your custom options instead of numeric values
- Nodes are bigger (800 size instead of 400) for better visibility
- Node colors still follow the ranking scheme (dark blue for rank ≤ edge)

### 3. Downloads (Tab: Downloads)
You now have 3 download options:

#### Download Frequency Table
- Shows frequency data with your custom labels in the State column
- CSV format with headers

#### Download Stream Data (Raw)
- Original stream data as generated (numeric 1 to Episode Options)
- CSV format

#### Download Stream by Ranked Order (NEW!)
- Shows selected items for each time step in ranked order
- Uses your custom labels if provided, numeric values if not
- Comma-separated values for each time step
- Includes a preview of the first 5 rows

## Example Workflow

### Scenario: Analyzing Fruit Preferences

**Settings:**
- Episode Length: 120
- Options to Select: 2
- Episode Options: 4
- Selection Probability: 0.95

**Custom Options (Ranked):**
1. Apple
2. Banana
3. Orange
4. Grape

**Results:**
- Frequency table shows states as "Apple", "Banana", "Orange", "Grape"
- Network graph nodes labeled with fruit names
- Downloads include fruit names in the stream data

### Scenario: Analyzing Web Events (Random Order)

**Settings:**
- Episode Length: 150
- Options to Select: 3
- Episode Options: 5
- Selection Probability: 0.90

**Custom Options (Random):**
- click_button
- form_submit
- page_load
- error_event
- timeout_event

**Results:**
- Labels are randomly assigned to states
- Each run produces the same random assignment (seed=42)
- All visualizations use the custom event names

## Technical Details

### State to Label Mapping

**Ranked Order:**
```python
unique_states = sorted(FTable['State'].unique())  # [1, 2, 3, ...]
for i, state in enumerate(unique_states):
    mapping[state] = provided_options[i]
```

**Random Order:**
```python
np.random.seed(42)  # Fixed seed for reproducibility
shuffled = np.random.permutation(provided_options)
for i, state in enumerate(sorted_unique_states):
    mapping[state] = shuffled[i]
```

### Label Display in Network Graph

```python
if option_labels_provided:
    node_labels[node] = option_labels[node]
else:
    node_labels[node] = str(node)  # Use numeric rank
```

## Tips & Best Practices

1. **Keep Labels Short**: Long labels may overlap in the network graph
2. **Use Meaningful Names**: Makes results more interpretable
3. **Consistent Format**: Use similar naming conventions (all caps, snake_case, etc.)
4. **Test with Defaults First**: Run once without custom options to understand the data, then add labels
5. **Download for Analysis**: Export CSV files for further analysis in Excel or Python

## Troubleshooting

### Issue: Some nodes missing labels
**Cause**: Not enough labels provided or labels are empty
**Solution**: Ensure you have exactly Episode Options number of labels entered

### Issue: Labels not showing in network graph
**Cause**: Labels might be too long or the expander wasn't properly closed
**Solution**: Shorten labels or click "Generate Analysis" again

### Issue: Different labels each run (with Random order selected)
**Cause**: This shouldn't happen - seed is fixed at 42
**Solution**: Clear browser cache and reload

## Advanced: Modifying the Seed

If you need different random assignments, you can edit the code:

In `streamlit_app.py`, find:
```python
np.random.seed(42)  # Fixed seed
```

Change 42 to any other number to get different random assignments.

## Future Enhancements

Potential features that could be added:
- [ ] Color-coding for different label categories
- [ ] Manual state-to-label mapping interface
- [ ] Import/export label configurations
- [ ] Label validation before analysis
- [ ] Batch processing with different configurations
