# Google Doc + Google Sheet setup (member-wise specs + restricted access)

## A) Create the Google Doc
1) Go to Google Drive → New → Google Docs.
2) Name it: `CSE423 Project Specs — Skydiving Simulator`.
3) Copy-paste the full content from PROJECT_SPECS_MEMBER_WISE.md into the Doc.

## B) Restrict sharing (ONLY group members + faculties)
1) Click Share (top-right).
2) Under “General access”, set to: `Restricted`.
3) Add group members (their Gmail) and set role:
   - If everyone must edit: set members to `Editor`.
   - If only 1 person compiles and others just view: set others to `Viewer` or `Commenter`.
4) Add faculty emails and set role as required by your course:
   - If faculty needs edit access: `Editor`.
   - If faculty only needs view access: `Viewer`.
5) Make sure:
   - “Anyone with the link” is NOT enabled.
   - “Editors can change permissions and share” is disabled (optional but safer).

## C) Get the Doc link
1) Share → Copy link.
2) The link will work only for the added emails (because access is Restricted).

Paste final Doc link here:
- Google Doc link: ______________________________

## D) Create the Google Sheet (to submit link)
1) Google Drive → New → Google Sheets.
2) Name it: `CSE423 Project Submission Links`.
3) Create columns:
   - Group No.
   - Member 1 Name
   - Member 1 Email
   - Member 2 Name
   - Member 2 Email
   - Faculty Email(s)
   - Google Doc Link
   - GitHub/Zip Link (if required)
   - Notes
4) Paste your Doc link in the “Google Doc Link” column.

## E) Apply the same sharing restrictions to the Sheet
1) Share → set “General access” to `Restricted`.
2) Add the same members + faculty with the required role.

Paste final Sheet link here:
- Google Sheet link: _____________________________

## F) Quick verification checklist
- Open the Doc link in an Incognito/private window (not logged in) → should NOT open.
- Open while logged into a member account → should open.
- Confirm faculty account can view/edit as required.
