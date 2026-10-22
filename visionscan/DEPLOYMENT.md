# Deployment Guide

## 1. Push to GitHub
Create an empty repository on github.com (e.g. `visionscan`, public, no README), then in the `visionscan` folder:

```bash
git init
git add .
git commit -m "VisionScan: object detection app"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/visionscan.git
git push -u origin main
```

## 2. Deploy on Streamlit Community Cloud (gives the live link)
1. Go to https://share.streamlit.io and sign in with GitHub.
2. Click **Create app** → "Deploy a public app from GitHub".
3. Choose your repository, branch `main`, main file path `app.py`.
4. Open **Advanced settings** → select **Python 3.11**.
5. Click **Deploy**. The first build takes several minutes (PyTorch + YOLO download).
6. Your link looks like `https://YOUR-APP-NAME.streamlit.app` – put it in `README.md`.

## 3. If the build fails
- **Out of memory / app restarts:** the free tier has ~1 GB RAM. Use `yolov8n.pt` (the default) and avoid selecting `yolov8s.pt`; process shorter videos.
- **`libGL.so.1` missing / `ImportError: libGL`:** check that `packages.txt` exists in the repo root and contains `libgl1` and `libglib2.0-0`; make sure `opencv-python-headless` (not `opencv-python`) is in `requirements.txt`.
- **Install too slow / disk full:** make sure the first line of `requirements.txt` is `--extra-index-url https://download.pytorch.org/whl/cpu` so the small CPU build of PyTorch is used.
- After fixing, commit + push; Streamlit Cloud redeploys automatically (or use **Reboot app**).

## 4. Backup: Hugging Face Spaces (Docker)
1. Create an account at https://huggingface.co and click **New Space**.
2. Choose **Docker** as the SDK (blank template) and create it.
3. Add this to the top of `README.md` in the Space repo:
   ```
   ---
   title: VisionScan
   sdk: docker
   app_port: 7860
   ---
   ```
4. Push the project (the `Dockerfile` is already included; it runs
   `streamlit run app.py --server.port 7860 --server.address 0.0.0.0`):
   ```bash
   git remote add space https://huggingface.co/spaces/YOUR-USERNAME/visionscan
   git push space main
   ```
5. The Space builds and gives you a link like `https://huggingface.co/spaces/YOUR-USERNAME/visionscan`.

## 5. Submission checklist
- [ ] Project zip (without `.venv/`)
- [ ] GitHub repository link
- [ ] Live app link (Streamlit Cloud, or Hugging Face as backup)
- [ ] Screenshots added to `README.md`
- [ ] Team / Author section in `pages/5_About.py` filled in
