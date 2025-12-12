# How to Deploy Your Cosmic To-Do App 🚀

To access your app 24/7 without keeping your laptop on, you need to "host" it on a server in the cloud.

The easiest (and usually free) way for this app is to use **Ren**der** or **Railway**.

## Option 1: Render (Recommended for simplicity)

1.  **Push your code** to GitHub.
    *   Initialize git: `git init`
    *   Add files: `git add .`
    *   Commit: `git commit -m "Initial commit"`
    *   Create a repo on GitHub and follow instructions to push.
2.  **Sign up** at [render.com](https://render.com).
3.  Click **"New +"** -> **"Web Service"**.
4.  Connect your GitHub repository.
5.  Render will auto-detect Python.
    *   **Build Command**: `pip install -r requirements.txt`
    *   **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6.  Click **Create Web Service**.

*Note: On the free tier, your tasks (data) might reset if the app restarts because Render's free filesystem is "ephemeral".*

## Option 2: PythonAnywhere (Better for saving data)

1.  Sign up at [pythonanywhere.com](https://www.pythonanywhere.com/).
2.  Go to "Web" tab -> "Add a new web app".
3.  Choose **FastAPI** (if available) or Manual Configuration.
4.  Upload your files using the "Files" tab.
5.  This platform keeps your `tasks.txt` file safe even after restarts!

## Option 3: Use a Database (Advanced)

To make your data permanent on any cloud platform, we would need to switch from `tasks.txt` to a database like **PostgreSQL** or **MongoDB**. Let me know if you want to make that upgrade!
