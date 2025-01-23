# INSERT-Speeds-up ✨

This is a Flask application that allows you to generate INSERT scripts for SQL Server from CSV or XLSX files. The project simplifies the creation of bulk insertion scripts by offering an intuitive web interface and data processing capabilities.

---

## Key Features

- 📃 Support for CSV and XLSX files
- 🌐 User-friendly web interface
- ⚙️ Batch SQL script generation
- 🔄 Handling of different data types
- 📥 Downloadable generated scripts

---

## System Requirements

- Python 3.8+
- Libraries listed in `requirements.txt`

---

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/joaooliveira10/INSERT-Speeds-up.git
   cd INSERT-Speeds-up
   ```

2. Create a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

---

## Configuration

### `requirements.txt`
```
flask
pandas
openpyxl
sqlalchemy
```

---

## Running the Application

```bash
python app.py
```

Access in your browser: `http://localhost:5000`

---

## Usage

1. Enter the table name.
2. Specify the columns (comma-separated, no spaces).
3. Upload the CSV or XLSX file.
4. Click "Generate Scripts."

### Example Input File

| name   | age | city       |
|--------|-----|------------|
| John   | 30  | New York   |
| Maria  | 25  | San Diego  |

### Example Interface Usage

- **Table Name**: users
- **Columns**: name, age, city
- **File**: spreadsheet.xlsx

---

## Known Limitations

- Limited support for complex data types
- No direct database connection
- Scripts should be reviewed before production use

---

## Security

- File upload validation
- Special character handling
- Secure script generation

---

## Contribution

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request


---

## Contact

[joaoangello10@gmail.com]

---

## Bonus: SQL Synchronization Script 🏛

### Context

Previously, I developed a procedure to check identical tables in different databases on the same SQL Server instance. It is efficient and practical for data synchronization. However, a situation arose in which I did not have access to another bank and I needed to resolve this situation in another way.

### Script Example

```sql
-- Check if the table exists in both databases
IF NOT EXISTS (SELECT * FROM [xxxdb].sys.objects WHERE object_id = OBJECT_ID(N'[xxxdb].[dbo].[tbyyy]') AND type in (N'U'))       -- FROM [xxxdb] or FROM [192.168.xxx.xxx].[xxxdb]
BEGIN
    RAISERROR ('Table tbyyy does not exist in database xxxdb', 16, 1)
    RETURN
END

IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[tbyyy]') AND type in (N'U'))                       -- FROM [xxxdb] or FROM [192.168.xxx.xxx].[xxxdb]
BEGIN
    RAISERROR ('Table tbyyy does not exist in the source database', 16, 1)
    RETURN
END

BEGIN TRY
    BEGIN TRANSACTION;

    -- Count inserted records
    DECLARE @InsertedRecords INT;

    -- Insert missing records
    -- INSERT INTO [xxxdb].[dbo].[tbyyy] (ID, Name, Description, DocumentTypeID)                                                 -- [xxxdb] or  [192.168.xxx.xxx].[xxxdb]
    SELECT
        src.ID,
        src.Name,
        src.Description,
        src.DocumentTypeID
    FROM [dbo].[tbyyy] AS src                                                                                                    -- FROM [xxxdb] or FROM [192.168.xxx.xxx].[xxxdb]
    LEFT JOIN [xxxdb].[dbo].[tbyyy] AS dest
        ON src.Name = dest.Name COLLATE Latin1_General_CI_AS
        AND src.DocumentTypeID = dest.DocumentTypeID
    WHERE dest.Name IS NULL
        AND dest.DocumentTypeID IS NULL;

    -- Number of inserted records
    SET @InsertedRecords = @@ROWCOUNT;

    -- Commit only if records were inserted
    IF @InsertedRecords > 0
    BEGIN
        COMMIT TRANSACTION;
        PRINT 'Synchronization completed successfully. ' + CAST(@InsertedRecords AS VARCHAR(10)) + ' record(s) inserted.';
    END
    ELSE
    BEGIN
        ROLLBACK TRANSACTION;
        PRINT 'No new records to insert.';
    END

END TRY
BEGIN CATCH
    IF @@TRANCOUNT > 0
        ROLLBACK TRANSACTION;

    DECLARE @ErrorMessage NVARCHAR(4000) = ERROR_MESSAGE();
    DECLARE @ErrorSeverity INT = ERROR_SEVERITY();
    DECLARE @ErrorState INT = ERROR_STATE();

    RAISERROR (@ErrorMessage, @ErrorSeverity, @ErrorState);
END CATCH;
```

