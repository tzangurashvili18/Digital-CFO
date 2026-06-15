# Commschool · Digital CFO

Internal financial dashboard for Commschool — courses P&L, corporate projects, fixed costs, and consolidated dashboard.

## Setup

```bash
npm install
npm start
```

Opens at http://localhost:3000

## Deploy to GitHub Pages (free, shareable URL)

1. Add to `package.json`:
   ```json
   "homepage": "https://YOUR_GITHUB_USERNAME.github.io/commschool-cfo"
   ```

2. Install gh-pages:
   ```bash
   npm install --save-dev gh-pages
   ```

3. Add to `package.json` scripts:
   ```json
   "predeploy": "npm run build",
   "deploy": "gh-pages -d build"
   ```

4. Deploy:
   ```bash
   npm run deploy
   ```

Your app will be live at the homepage URL above.

## Stack
- React 18
- Tailwind CSS
- No backend — all data is in-app state
