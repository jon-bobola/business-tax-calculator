import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple, Union


class TaxVisualization:
    """Visualization utilities for tax calculation results."""
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize with analysis results DataFrame.
        
        Args:
            df: DataFrame containing tax calculation results
        """
        # Store both a formatted (display) version and a numeric version for plotting
        self.display_df = df.copy()
        self.numeric_df = self._convert_to_numeric(df)
        # Set standard figure size and styling
        plt.rcParams["figure.figsize"] = (12, 7)
        sns.set_style("whitegrid")
        
    def _convert_to_numeric(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Convert formatted money columns to numeric values for plotting.
        
        Args:
            df: DataFrame with formatted values
            
        Returns:
            DataFrame with numeric values
        """
        numeric_df = df.copy()
        
        # Convert money columns (columns with $ format)
        money_cols = [
            col for col in numeric_df.columns 
            if isinstance(numeric_df[col].iloc[0], str) and "$" in str(numeric_df[col].iloc[0])
        ]
        
        for col in money_cols:
            numeric_df[col] = numeric_df[col].str.replace('$', '').str.replace(',', '').astype(float)
            
        # Convert percentage columns
        pct_cols = [
            col for col in numeric_df.columns 
            if isinstance(numeric_df[col].iloc[0], str) and "%" in str(numeric_df[col].iloc[0])
        ]
        
        for col in pct_cols:
            numeric_df[col] = numeric_df[col].str.replace('%', '').astype(float)
            
        return numeric_df
    
    def plot_tax_comparison(self, save_path: Optional[str] = None) -> None:
        """
        Plot total tax comparison between entity types.
        
        Args:
            save_path: Optional path to save the plot
        """
        # Create pivot table for comparison
        pivot = self.numeric_df.pivot(
            index="Net Revenue", 
            columns="Entity Type", 
            values="Total Tax"
        )
        
        # Plot
        ax = pivot.plot(kind='bar', figsize=(12, 7))
        ax.set_title('Total Tax Comparison by Entity Type', fontsize=16)
        ax.set_ylabel('Total Tax ($)', fontsize=14)
        ax.set_xlabel('Net Revenue ($)', fontsize=14)
        
        # Format y-axis ticks as currency
        ax.yaxis.set_major_formatter('${x:,.0f}')
        
        # Add value labels on top of bars
        for container in ax.containers:
            ax.bar_label(container, fmt='${:,.0f}')
        
        plt.legend(title="Entity Type")
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path)
        
        plt.show()
        
    def plot_tax_breakdown(self, revenue_level: float, save_path: Optional[str] = None) -> None:
        """
        Plot tax breakdown pie charts for each entity type at a specific revenue level.
        
        Args:
            revenue_level: Net revenue level to compare
            save_path: Optional path to save the plot
        """
        # Filter the dataset to the specified revenue level
        filtered_df = self.numeric_df[self.numeric_df["Net Revenue"] == revenue_level]
        
        if filtered_df.empty:
            closest_revenue = self.numeric_df["Net Revenue"].iloc[
                (self.numeric_df["Net Revenue"] - revenue_level).abs().argsort()[0]
            ]
            print(f"No data for revenue level {revenue_level}. Using closest revenue: {closest_revenue}")
            filtered_df = self.numeric_df[self.numeric_df["Net Revenue"] == closest_revenue]
            revenue_level = closest_revenue
            
        entity_types = filtered_df["Entity Type"].unique()
        
        # Set up the figure
        fig, axs = plt.subplots(1, len(entity_types), figsize=(7*len(entity_types), 7))
        if len(entity_types) == 1:
            axs = [axs]
            
        # Tax components to include
        tax_components = [
            "Social Security Tax", "Medicare Tax", "Federal Tax", "State Tax", "Local Tax"
        ]
            
        # Plot pie chart for each entity type
        for i, entity_type in enumerate(entity_types):
            entity_data = filtered_df[filtered_df["Entity Type"] == entity_type]
            
            # Extract tax components
            tax_values = [entity_data[component].iloc[0] for component in tax_components]
            
            # Plot
            axs[i].pie(
                tax_values,
                labels=tax_components,
                autopct='%1.1f%%',
                startangle=90,
                shadow=True,
            )
            axs[i].set_title(f"{entity_type} - ${revenue_level:,.0f} Net Revenue\nTotal Tax: ${sum(tax_values):,.0f}")
            
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path)
            
        plt.show()
        
    def plot_effective_tax_rate(self, save_path: Optional[str] = None) -> None:
        """
        Plot effective tax rate comparison between entity types.
        
        Args:
            save_path: Optional path to save the plot
        """
        # Calculate effective tax rates
        df = self.numeric_df.copy()
        df['Effective Tax Rate'] = (df['Total Tax'] / df['Net Revenue']) * 100
        
        # Create pivot table
        pivot = df.pivot(
            index="Net Revenue",
            columns="Entity Type",
            values="Effective Tax Rate"
        )
        
        # Plot
        ax = pivot.plot(kind='line', marker='o', figsize=(12, 7))
        ax.set_title('Effective Tax Rate Comparison', fontsize=16)
        ax.set_ylabel('Effective Tax Rate (%)', fontsize=14)
        ax.set_xlabel('Net Revenue ($)', fontsize=14)
        
        # Format x-axis ticks as currency
        ax.xaxis.set_major_formatter('${x:,.0f}')
        
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
        
        plt.grid(True)
        plt.legend(title="Entity Type")
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path)
            
        plt.show()
        
    def plot_tax_savings(self, save_path: Optional[str] = None) -> None:
        """
        Plot tax savings of S-Corp vs Sole Proprietor.
        
        Args:
            save_path: Optional path to save the plot
        """
        # Get absolute tax differences
        df = self.numeric_df.copy()
        
        # Create pivoted data for comparison
        pivot = df.pivot(
            index="Net Revenue",
            columns="Entity Type",
            values="Total Tax"
        )
        
        # Calculate differences
        if "S Corporation" in pivot.columns and "Sole Proprietor" in pivot.columns:
            savings = pivot["Sole Proprietor"] - pivot["S Corporation"]
            
            # Plot
            ax = savings.plot(kind='bar', figsize=(12, 7), color='green')
            ax.set_title('Tax Savings: S Corporation vs Sole Proprietor', fontsize=16)
            ax.set_ylabel('Tax Savings ($)', fontsize=14)
            ax.set_xlabel('Net Revenue ($)', fontsize=14)
            
            # Format y-axis ticks as currency
            ax.yaxis.set_major_formatter('${x:,.0f}')
            
            # Add value labels
            for i, v in enumerate(savings):
                ax.text(
                    i, v + 0.1,
                    f'${v:,.0f}',
                    ha='center',
                    fontweight='bold'
                )
            
            plt.tight_layout()
            
            if save_path:
                plt.savefig(save_path)
                
            plt.show()
        else:
            print("Both 'S Corporation' and 'Sole Proprietor' entity types are required for this plot")
            
    def plot_deduction_comparison(self, save_path: Optional[str] = None) -> None:
        """
        Plot deduction comparison between entity types.
        
        Args:
            save_path: Optional path to save the plot
        """
        # Deduction components to include
        deduction_components = [
            "Standard Deduction", "Social Security Deduction", 
            "Medicare Deduction", "QBI Deduction"
        ]
        
        # Set up the figure based on number of revenue levels
        revenue_levels = self.numeric_df["Net Revenue"].unique()
        n_revenues = len(revenue_levels)
        n_cols = min(3, n_revenues)
        n_rows = (n_revenues + n_cols - 1) // n_cols
        
        fig, axs = plt.subplots(n_rows, n_cols, figsize=(7*n_cols, 7*n_rows))
        if n_rows * n_cols == 1:
            axs = np.array([[axs]])
        elif n_rows == 1 or n_cols == 1:
            axs = axs.reshape(n_rows, n_cols)
            
        # Plot for each revenue level
        for i, revenue in enumerate(sorted(revenue_levels)):
            row, col = i // n_cols, i % n_cols
            ax = axs[row, col]
            
            # Filter data for this revenue level
            filtered_df = self.numeric_df[self.numeric_df["Net Revenue"] == revenue]
            
            # Prepare data for grouped bar chart
            entity_types = filtered_df["Entity Type"].unique()
            x = np.arange(len(deduction_components))
            width = 0.8 / len(entity_types)
            
            for j, entity_type in enumerate(entity_types):
                entity_data = filtered_df[filtered_df["Entity Type"] == entity_type]
                values = [entity_data[component].iloc[0] for component in deduction_components]
                
                offset = j * width - width * (len(entity_types) - 1) / 2
                bars = ax.bar(x + offset, values, width, label=entity_type)
                
                # Add value labels
                for bar in bars:
                    height = bar.get_height()
                    ax.text(
                        bar.get_x() + bar.get_width() / 2,
                        height + 100,
                        f'${height:,.0f}',
                        ha='center',
                        va='bottom',
                        rotation=45,
                        fontsize=8
                    )
            
            # Customize the plot
            ax.set_title(f'Net Revenue: ${revenue:,.0f}')
            ax.set_xticks(x)
            ax.set_xticklabels(deduction_components, rotation=45, ha='right')
            ax.set_ylabel('Amount ($)')
            
            # Only add legend to the first subplot
            if i == 0:
                ax.legend(title="Entity Type")
                
        # Hide unused subplots
        for i in range(n_revenues, n_rows * n_cols):
            row, col = i // n_cols, i % n_cols
            axs[row, col].axis('off')
                
        plt.tight_layout()
        fig.suptitle('Deduction Comparison by Entity Type', fontsize=16, y=1.02)
        
        if save_path:
            plt.savefig(save_path, bbox_inches='tight')
            
        plt.show()
        
    def generate_report(self, output_dir: str = "./tax_report") -> None:
        """
        Generate a comprehensive visual report with all plots.
        
        Args:
            output_dir: Directory to save report plots
        """
        import os
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate all plots
        print("Generating tax comparison plot...")
        self.plot_tax_comparison(save_path=f"{output_dir}/tax_comparison.png")
        
        print("Generating effective tax rate plot...")
        self.plot_effective_tax_rate(save_path=f"{output_dir}/effective_tax_rate.png")
        
        print("Generating tax savings plot...")
        self.plot_tax_savings(save_path=f"{output_dir}/tax_savings.png")
        
        print("Generating deduction comparison plot...")
        self.plot_deduction_comparison(save_path=f"{output_dir}/deduction_comparison.png")
        
        # Generate tax breakdown for each revenue level
        for revenue in self.numeric_df["Net Revenue"].unique():
            print(f"Generating tax breakdown for ${revenue:,.0f}...")
            self.plot_tax_breakdown(
                revenue_level=revenue,
                save_path=f"{output_dir}/tax_breakdown_{int(revenue)}.png"
            )
            
        print(f"Report generation complete. Files saved to {output_dir}")