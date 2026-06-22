@echo off
REM Batch file with various Odoo password reset commands

echo === Odoo Password Reset Commands ===
echo.

echo Method 1: Using Python script (Recommended)
echo python reset_password.py [database_name] admin@adigielite.com [new_password]
echo.

echo Method 2: Using Odoo Shell
echo python -m odoo shell -d [database_name] -c odoo.conf
echo Then run the commands from odoo_shell_commands.txt
echo.

echo Method 3: Using main odoo module
echo python -m odoo -d [database_name] -c odoo.conf --shell
echo.

echo Method 4: Direct execution with Python
echo python -c "import sys, os; sys.path.insert(0, '.'); exec(open('reset_password.py').read().replace('if __name__ == \"__main__\":', 'if True:'))" [database_name] admin@adigielite.com [new_password]
echo.

echo Replace [database_name] with your actual database name
echo Replace [new_password] with your desired password
echo.

pause