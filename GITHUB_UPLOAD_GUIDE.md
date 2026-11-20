# Publish this project to GitHub

The project is prepared for GitHub, but an online repository is not created automatically. Create it in your own GitHub account:

1. Sign in at https://github.com/
2. Select **New repository**.
3. Repository name: `Student_Result_Manager`
4. Choose Public or Private according to your teacher's instruction.
5. Do not initialize with a README, license or `.gitignore` (these are already in this project).
6. Create the repository and copy its HTTPS URL.

Then open the `Student_Result_Manager` folder in VS Code and run these commands in its terminal:

```bash
git init
git add .
git commit -m "Initial Student Result Manager project"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/Student_Result_Manager.git
git push -u origin main
```

Replace `YOUR-USERNAME` with your GitHub username and use the repository URL copied from GitHub.

After pushing, open the repository page and confirm that `main.py`, `student_manager.py`, `tests/`, `UML/`, `README.md` and `PROJECT_REPORT.md` are visible. Submit that repository URL to your teacher.
