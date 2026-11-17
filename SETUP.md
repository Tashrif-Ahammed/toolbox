> Auto setup: run Toolbox-Setup.bat once and it does everything below for you. This file is only for manual setup.

# Toolbox: GitHub e chalano (ধাপে ধাপে)

## ১. GitHub repo বানাও
1. github.com এ **New repository** চাপো। নাম দাও `toolbox`, **Public** রাখো, Create করো।
2. **uploading an existing file** চাপো। এই ফোল্ডারের **সব ফাইল ও tools, icons ফোল্ডার** ড্র্যাগ করে দাও (`.nojekyll` ফাইলটা hidden থাকলে বাদ গেলেও চলবে)।
3. **Commit changes** চাপো।

## ২. Pages চালু করো
Repo > **Settings > Pages > Source: Deploy from a branch > main > /(root) > Save**।
১-২ মিনিট পর সাইট খুলবে: `https://তোমার-নাম.github.io/toolbox/`

## ৩. Admin token বানাও
1. GitHub > ছবিতে ক্লিক > **Settings > Developer settings > Personal access tokens > Fine-grained tokens > Generate new token**
2. Name: `toolbox`, Expiration: ১ বছর
3. **Repository access: Only select repositories** > `toolbox`
4. **Permissions > Repository permissions > Contents: Read and write**
5. Generate করে token কপি করো (`github_pat_...`)। এটা আর দ্বিতীয়বার দেখাবে না।

## ৪. সাইটে Admin হও
সাইটে গিয়ে ⚙ Settings খোলো > **GitHub Sync** > Repository ঘরে `তোমার-নাম/toolbox` > token paste > **Connect**।
"Connected as admin" দেখালে হয়ে গেছে। এখন Add Tool, Edit, Archive, Delete, Categories সব কাজ করবে এবং নিজে থেকে GitHub এ save হবে (উপরে "Synced to GitHub" লেখা আসবে)।
token শুধু ওই ব্রাউজারে থাকে। অন্য পিসি/ফোনে একই কাজ আবার করতে হবে।

## ৫. আগের পিসির Category/আইকন/বিবরণ আনো
1. পুরনো localhost ড্যাশবোর্ডে ⚙ Settings > **Export backup**
2. নতুন সাইটে (Admin অবস্থায়) ⚙ Settings > **Import backup** > ওই ফাইল দাও
3. সব নিজে থেকে GitHub এ save হবে।

## দৈনন্দিন কাজ
- **নতুন টুল:** ＋ Add Tool > Upload বা Paste। Save হলে GitHub এ commit হয়।
- **আপডেট:** একই নামে আবার আপলোড করলে ফাইল বদলে যায়।
- **GitHub এ সরাসরি ফাইল তুললে:** `tools/` এ ফাইল দিয়ে সাইটে ↻ Scan চাপো। নতুন ফাইল নিজে থেকে যোগ হবে।
- **Permanently delete করলে** ফাইলটা repo থেকেও মুছে যায়। ফেরত আনতে GitHub এর commit history ব্যবহার করতে হবে।

## জেনে রাখো
- নতুন ফাইল সবার কাছে লাইভ হতে ১-২ মিনিট লাগে।
- Pages এ ঘণ্টায় ১০টার মতো বিল্ডের নরম সীমা আছে। ঘন ঘন বদল করলে মাঝে মাঝে দেরি হতে পারে।
- `server-loop.bat`, `run-hidden.vbs` আর `data` শর্টকাট এখন লাগবে না।
