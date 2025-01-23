import os
import pandas as pd
from flask import Flask, render_template, request, send_from_directory, flash, redirect, url_for
from werkzeug.utils import secure_filename

class SQLScriptGenerator:
    def __init__(self, upload_folder='uploads', download_folder='download'):
        self.upload_folder = upload_folder
        self.download_folder = download_folder
        os.makedirs(upload_folder, exist_ok=True)
        os.makedirs(download_folder, exist_ok=True)

    def validate_dataframe(self, df, required_columns):
        """Valida colunas e tipos de dados"""
        missing_columns = set(required_columns) - set(df.columns)
        if missing_columns:
            raise ValueError(f"Colunas faltando: {missing_columns}")
        return df[required_columns]

    def generate_insert_scripts(self, df, table_name, columns, batch_size=1000):
        """Gera scripts SQL com tratamento de tipos"""
        scripts = []
        for i in range(0, len(df), batch_size):
            batch = df[i:i+batch_size]
            
            for _, row in batch.iterrows():
                values = []
                for col in columns:
                    val = row[col]
                    if pd.isna(val):
                        values.append('NULL')
                    elif isinstance(val, str):
                        val = val.replace("'", "''")
                        values.append(f"'{val}'")
                    elif isinstance(val, (int, float)):
                        values.append(str(val))
                    else:
                        values.append(f"'{str(val)}'")
                
                script = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(values)});"
                scripts.append(script)
        
        return scripts

    def save_scripts(self, scripts, filename='inserts.sql'):
        """Salva scripts na pasta de download"""
        output_file = os.path.join(self.download_folder, filename)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(scripts))
        return output_file

    def read_file(self, file):
        """Lê arquivo CSV ou XLSX"""
        filename = secure_filename(file.filename)
        file_path = os.path.join(self.upload_folder, filename)
        file.save(file_path)
        
        try:
            if filename.endswith('.csv'):
                return pd.read_csv(file_path, encoding='utf-8')
            else:
                return pd.read_excel(file_path)
        except Exception as e:
            raise ValueError(f"Erro ao processar arquivo: {e}")

def create_app():
    app = Flask(__name__)
    app.secret_key = os.urandom(24)
    generator = SQLScriptGenerator()

    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'POST':
            try:
                table_name = request.form['table_name']
                columns = [col.strip() for col in request.form['columns'].split(',')]
                file = request.files['file']

                # Ler e validar arquivo
                df = generator.read_file(file)
                df = generator.validate_dataframe(df, columns)

                # Gerar scripts
                scripts = generator.generate_insert_scripts(df, table_name, columns)
                output_filename = f"{table_name}_inserts.sql"
                generator.save_scripts(scripts, output_filename)

                flash(f"Gerados {len(scripts)} scripts de insert")
                return render_template('result.html', 
                                       scripts=scripts[:50],  
                                       total_scripts=len(scripts),
                                       filename=output_filename)
            
            except Exception as e:
                flash(f"Erro: {str(e)}")
                return redirect(url_for('index'))
        
        return render_template('index.html')

    @app.route('/download/<filename>')
    def download_sql(filename):
        return send_from_directory(generator.download_folder, filename, as_attachment=True)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)