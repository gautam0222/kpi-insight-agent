import pandas as pd
from openai import OpenAI
from kpi_intel.app.core.config import config
from kpi_intel.app.core.data_loader import data_loader
from kpi_intel.app.core.logger import logger

class TalkToDataAgent:
    def __init__(self):
        self.client = OpenAI(
            base_url=config.OPENROUTER_BASE_URL,
            api_key=config.OPENROUTER_API_KEY
        )
        self.df = data_loader.get_data()
    
    def query(self, question):
        """Process natural language question and return answer"""
        logger.info(f"Talk-to-Data query: {question}")
        
        # Get data schema
        schema = self._get_schema()
        
        # Generate pandas code using LLM
        code = self._generate_code(question, schema)
        
        # Execute code safely
        result = self._execute_code(code)
        
        # Generate explanation
        explanation = self._generate_explanation(question, result, code)
        
        logger.info(f"Query result: {result}")
        
        return {
            'result': result,
            'explanation': explanation,
            'code': code
        }
    
    def _get_schema(self):
        """Get dataframe schema info"""
        schema = f"""
DataFrame Shape: {self.df.shape}
Columns: {list(self.df.columns)}
Date Range: {self.df['Date'].min()} to {self.df['Date'].max()}
Sample Data:
{self.df.head(3).to_string()}
"""
        return schema
    
    def _generate_code(self, question, schema):
        """Generate pandas code using LLM"""
        prompt = f"""You are a data analyst. Given this DataFrame schema and a user question, generate ONLY the Python pandas code to answer it.

{schema}

Important columns:
- Overall_Revenue: Total revenue (Sales_y + Sales_m)
- Date: Transaction date
- Product_Name, Category, Sub_category: Product info
- Discount, M_Spend (Marketing Spend), Supply_Chain_E (Supply Chain Efficiency)

User Question: {question}

Return ONLY executable Python code using 'df' as the DataFrame variable. No explanations, no markdown, just code.
Example: df.groupby('Category')['Overall_Revenue'].sum().sort_values(ascending=False).head(5)
"""
        
        try:
            response = self.client.chat.completions.create(
                model=config.OPENROUTER_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0
            )
            
            code = response.choices[0].message.content.strip()
            # Clean code
            code = code.replace('```python', '').replace('```', '').strip()
            
            return code
        except Exception as e:
            logger.error(f"Error generating code: {e}")
            return None
    
    def _execute_code(self, code):
        """Safely execute generated pandas code"""
        if not code:
            return "Could not generate code for this query."
        
        try:
            # Create safe execution environment
            df = self.df.copy()
            local_vars = {'df': df, 'pd': pd}
            
            # Execute code
            result = eval(code, {"__builtins__": {}}, local_vars)
            
            # Format result
            if isinstance(result, pd.DataFrame):
                return result.to_string()
            elif isinstance(result, pd.Series):
                return result.to_string()
            else:
                return str(result)
                
        except Exception as e:
            logger.error(f"Error executing code: {e}")
            return f"Error executing query: {str(e)}"
    
    def _generate_explanation(self, question, result, code):
        """Generate human-readable explanation"""
        prompt = f"""Given this data query and result, provide a brief business explanation (2-3 sentences).

Question: {question}
Code executed: {code}
Result: {result}

Provide a clear, concise explanation of what the data shows."""
        
        try:
            response = self.client.chat.completions.create(
                model=config.OPENROUTER_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Error generating explanation: {e}")
            return "Data retrieved successfully."

agent = TalkToDataAgent()