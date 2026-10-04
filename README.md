# 𝔸𝔹𝔻𝕆𝕌𝕌𝕌 ℍ𝕌𝕊𝔼ℕ𝔾 𝕍ℙ𝕊

Flask + SQLite hosting landing page with activation-code management.

## Run
```bash
pip install -r requirements.txt
python app.py
```

## Admin
The admin URL is controlled by `ADMIN_PATH`.
Set a long random path before deployment, for example:
`ADMIN_PATH=abdouuu-admin-9f3d2a7c`

The requested design uses a private admin URL without a password. Anyone who discovers that URL can access admin, so keep it secret.

## Code format
All generated codes start with:
`ABDOUUU-HUSENG-VPS-`

The admin can choose expiry in days and maximum user activations.


## رابط لوحة الإدارة
`/abdouuu-vps-cod`
