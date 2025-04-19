import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk
from tkinter import ttk
import numpy as np
from typing import List, Callable, Dict, Any

class TaxVisualizationViewer:
    """Interactive viewer for tax visualizations with navigation controls."""
    
    def __init__(self, tax_data_df):
        """
        Initialize the visualization viewer.
        
        Args:
            tax_data_df: DataFrame with tax calculation results
        """
        self.df = tax_data_df
        self.visualizations = []
        self.current_index = 0
        
        # Set up the main window
        self.root = tk.Tk()
        self.root.title("Tax Scenario Visualization Browser")
        self.root.geometry("1200x800")
        
        # Configure the main frame
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create the visualization title
        self.title_var = tk.StringVar()
        self.title_label = ttk.Label(
            self.main_frame, 
            textvariable=self.title_var,
            font=('Helvetica', 16, 'bold')
        )
        self.title_label.pack(pady=(0, 10))
        
        # Create the matplotlib figure and canvas
        self.fig = plt.Figure(figsize=(10, 6), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.main_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Add navigation toolbar
        self.toolbar_frame = ttk.Frame(self.main_frame)
        self.toolbar_frame.pack(fill=tk.X)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.toolbar_frame)
        self.toolbar.update()
        
        # Create navigation controls
        self.nav_frame = ttk.Frame(self.main_frame)
        self.nav_frame.pack(fill=tk.X, pady=10)
        
        # Add navigation buttons
        self.prev_btn = ttk.Button(
            self.nav_frame, 
            text="← Previous",
            command=self.show_previous
        )
        self.prev_btn.pack(side=tk.LEFT)
        
        self.position_label_var = tk.StringVar()
        self.position_label = ttk.Label(
            self.nav_frame,
            textvariable=self.position_label_var,
            width=20,
            anchor=tk.CENTER
        )
        self.position_label.pack(side=tk.LEFT, expand=True)
        
        self.next_btn = ttk.Button(
            self.nav_frame, 
            text="Next →",
            command=self.show_next
        )
        self.next_btn.pack(side=tk.RIGHT)
        
        # Register visualizations
        self._register_visualizations()
        
        # Show first visualization
        self.show_visualization(0)
    
    def _register_visualizations(self):
        """Register all available visualizations."""
        self._add_visualization(
            "Total Tax Comparison", 
            self._create_tax_comparison_plot
        )
        
        self._add_visualization(
            "Effective Tax Rate Comparison", 
            self._create_effective_tax_rate_plot
        )
        
        self._add_visualization(
            "Tax Savings: S Corp vs Sole Proprietor", 
            self._create_tax_savings_plot
        )
        
        # Add breakdown visualizations for each revenue level
        for revenue in sorted(self.df["Net Revenue"].unique()):
            self._add_visualization(
                "Tax Breakdown - ${revenue:,.0f} Revenue",
                lambda rev=revenue: self._create_tax_breakdown_plot(rev)
            )
        
        self._add_visualization(
            "Deduction Comparison", 
            self._create_deduction_comparison_plot
        )
    
    def _add_visualization(self, title: str, plot_func: Callable):
        """
        Add a visualization to the viewer.
        
        Args:
            title: Title of the visualization
            plot_func: Function to create the visualization
        """
        self.visualizations.append({
            "title": title,
            "plot_func": plot_func
        })
    
    def show_visualization(self, index: int):
        """
        Show the visualization at the given index.
        
        Args:
            index: Index of the visualization to show
        """
        if 0 <= index < len(self.visualizations):
            self.current_index = index
            
            # Update the title
            self.title_var.set(self.visualizations[index]["title"])
            
            # Update position indicator
            self.position_label_var.set(f"{index + 1} / {len(self.visualizations)}")
            
            # Clear the figure
            self.fig.clear()
            
            # Create the new plot
            self.visualizations[index]["plot_func"]()
            
            # Update the canvas
            self.canvas.draw()
            
            # Update button states
            self.prev_btn["state"] = "normal" if index > 0 else "disabled"
            self.next_btn["state"] = "normal" if index < len(self.visualizations) - 1 else "disabled"
    
    def show_next(self):
        """Show the next visualization."""
        self.show_visualization(self.current_index + 1)
    
    def show_previous(self):
        """Show the previous visualization."""
        self.show_visualization(self.current_index - 1)
    
    def run(self):
        """Run the visualization viewer."""
        self.root.mainloop()
    
    # Visualization creation methods
    def _create_tax_comparison_plot(self):
        """Create tax comparison plot."""
        numeric_df = self._convert_to_numeric(self.df)
        
        # Create pivot table for comparison
        pivot = numeric_df.pivot(
            index="Net Revenue", 
            columns="Entity Type", 
            values="Total Tax"
        )
        
        # Plot
        ax = self.fig.add_subplot(111)
        pivot.plot(kind='bar', ax=ax)
        
        ax.set_title('Total Tax Comparison by Entity Type', fontsize=16)
        ax.set_ylabel('Total Tax ($)', fontsize=14)
        ax.set_xlabel('Net Revenue ($)', fontsize=14)
        
        # Format y-axis ticks as currency
        from matplotlib.ticker import FuncFormatter
        ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'${x:,.0f}'))
        
        # Add value labels on top of bars
        for container in ax.containers:
            ax.bar_label(container, fmt='${:,.0f}')
        
        ax.legend(title="Entity Type")
        self.fig.tight_layout()
    
    def _create_effective_tax_rate_plot(self):
        """Create effective tax rate plot."""
        numeric_df = self._convert_to_numeric(self.df)
        
        # Calculate effective tax rates
        df = numeric_df.copy()
        df['Effective Tax Rate'] = (df['Total Tax'] / df['Net Revenue']) * 100
        
        # Create pivot table
        pivot = df.pivot(
            index="Net Revenue",
            columns="Entity Type",
            values="Effective Tax Rate"
        )
        
        # Plot
        ax = self.fig.add_subplot(111)
        pivot.plot(kind='line', marker='o', ax=ax)
        
        ax.set_title('Effective Tax Rate Comparison', fontsize=16)
        ax.set_ylabel('Effective Tax Rate (%)', fontsize=14)
        ax.set_xlabel('Net Revenue ($)', fontsize=14)
        
        # Format x-axis ticks as currency
        from matplotlib.ticker import FuncFormatter
        ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f'${x:,.0f}'))
        
        # Add value labels
        for line, entity in zip(ax.lines, pivot.columns):
            for x, y in zip(line.get_xdata(), line.get_ydata()):
                ax.annotate(
                    f'{y:.1f}%', 
                    (x, y),
                    textcoords="offset points",
                    xytext=(0, 10),
                    ha='center'
                )
        
        ax.grid(True)
        ax.legend(title="Entity Type")
        self.fig.tight_layout()
    
    def _create_tax_savings_plot(self):
        """Create tax savings plot."""
        numeric_df = self._convert_to_numeric(self.df)
        
        # Create pivoted data for comparison
        pivot = numeric_df.pivot(
            index="Net Revenue",
            columns="Entity Type",
            values="Total Tax"
        )
        
        # Calculate differences
        if "S Corporation" in pivot.columns and "Sole Proprietor" in pivot.columns:
            savings = pivot["Sole Proprietor"] - pivot["S Corporation"]
            
            # Plot
            ax = self.fig.add_subplot(111)
            savings.plot(kind='bar', ax=ax, color='green')
            
            ax.set_title('Tax Savings: S Corporation vs Sole Proprietor', fontsize=16)
            ax.set_ylabel('Tax Savings ($)', fontsize=14)
            ax.set_xlabel('Net Revenue ($)', fontsize=14)
            
            # Format y-axis ticks as currency
            from matplotlib.ticker import FuncFormatter
            ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'${x:,.0f}'))
            
            # Add value labels
            for i, v in enumerate(savings):
                ax.text(
                    i, v + 0.1,
                    f'${v:,.0f}',
                    ha='center',
                    fontweight='bold'
                )
            
            self.fig.tight_layout()
        else:
            ax = self.fig.add_subplot(111)
            ax.text(
                0.5, 0.5,
                "Both 'S Corporation' and 'Sole Proprietor' entity types are required for this plot",
                ha='center',
                va='center',
                fontsize=14
            )
            ax.axis('off')
    
    def _create_tax_breakdown_plot(self, revenue_level: float):
        """Create tax breakdown plot for a specific revenue level."""
        numeric_df = self._convert_to_numeric(self.df)
        
        # Filter the dataset to the specified revenue level
        filtered_df = numeric_df[numeric_df["Net Revenue"] == revenue_level]
        
        if filtered_df.empty:
            closest_revenue = numeric_df["Net Revenue"].iloc[
                (numeric_df["Net Revenue"] - revenue_level).abs().argsort()[0]
            ]
            filtered_df = numeric_df[numeric_df["Net Revenue"] == closest_revenue]
            revenue_level = closest_revenue
            
        entity_types = filtered_df["Entity Type"].unique()
        
        # Tax components to include
        tax_components = [
            "Social Security Tax", "Medicare Tax", "Federal Tax", "State Tax", "Local Tax"
        ]
        
        # Set up subplots
        n_entities = len(entity_types)
        n_cols = min(n_entities, 3)
        n_rows = (n_entities + n_cols - 1) // n_cols
        
        for i, entity_type in enumerate(entity_types):
            entity_data = filtered_df[filtered_df["Entity Type"] == entity_type]
            
            # Extract tax components
            tax_values = [entity_data[component].iloc[0] for component in tax_components]
            
            # Create subplot
            ax = self.fig.add_subplot(n_rows, n_cols, i+1)
            
            # Plot pie chart
            wedges, texts, autotexts = ax.pie(
                tax_values,
                labels=tax_components,
                autopct='%1.1f%%',
                startangle=90,
                shadow=True,
            )
            
            # Make text more readable
            for text in texts + autotexts:
                text.set_fontsize(9)
            
            ax.set_title(f"{entity_type}\nTotal Tax: ${sum(tax_values):,.0f}")
        
        self.fig.suptitle(f'Tax Breakdown - ${revenue_level:,.0f} Net Revenue', fontsize=16)
        self.fig.tight_layout()
        self.fig.subplots_adjust(top=0.85)
    
    def _create_deduction_comparison_plot(self):
        """Create deduction comparison plot."""
        numeric_df = self._convert_to_numeric(self.df)
        
        # Deduction components to include
        deduction_components = [
            "Standard Deduction", "Social Security Deduction", 
            "Medicare Deduction", "QBI Deduction"
        ]
        
        # Set up the figure based on number of revenue levels
        revenue_levels = sorted(numeric_df["Net Revenue"].unique())
        n_revenues = len(revenue_levels)
        n_cols = min(2, n_revenues)
        n_rows = (n_revenues + n_cols - 1) // n_cols
        
        for i, revenue in enumerate(revenue_levels):
            row, col = i // n_cols, i % n_cols
            ax = self.fig.add_subplot(n_rows, n_cols, i+1)
            
            # Filter data for this revenue level
            filtered_df = numeric_df[numeric_df["Net Revenue"] == revenue]
            
            # Prepare data for grouped bar chart
            entity_types = filtered_df["Entity Type"].unique()
            x = np.arange(len(deduction_components))
            width = 0.8 / len(entity_types)
            
            for j, entity_type in enumerate(entity_types):
                entity_data = filtered_df[filtered_df["Entity Type"] == entity_type]
                values = [entity_data[component].iloc[0] for component in deduction_components]
                
                offset = j * width - width * (len(entity_types) - 1) / 2
                bars = ax.bar(x + offset, values, width, label=entity_type)
                
            # Customize the plot
            ax.set_title(f'Net Revenue: ${revenue:,.0f}')
            ax.set_xticks(x)
            ax.set_xticklabels([comp.split()[0] for comp in deduction_components], rotation=45, ha='right')
            ax.set_ylabel('Amount ($)')
            
            # Only add legend to the first subplot
            if i == 0:
                ax.legend(title="Entity Type")
                
        self.fig.suptitle('Deduction Comparison by Entity Type', fontsize=16)
        self.fig.tight_layout()
        self.fig.subplots_adjust(top=0.9)
    
    def _convert_to_numeric(self, df):
        """Convert formatted money columns to numeric values for plotting."""
        numeric_df = df.copy()
        
        # Try to convert all columns that appear to be money values
        for col in numeric_df.columns:
            try:
                if isinstance(numeric_df[col].iloc[0], str):
                    if "$" in numeric_df[col].iloc[0]:
                        numeric_df[col] = numeric_df[col].str.replace('$', '').str.replace(',', '').astype(float)
                    elif "%" in numeric_df[col].iloc[0]:
                        numeric_df[col] = numeric_df[col].str.replace('%', '').astype(float)
            except:
                # Skip if conversion fails
                continue
                
        return numeric_df