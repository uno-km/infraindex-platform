---
name: uppercase_system_code
description: Enforce ALL UPPERCASE for metadata and system code related database tables, columns, and records (SYS_CD_BAS, SYS_CD_GROUP_BAS).
---

# Uppercase System Code Rule

When creating, modifying, or populating data for the System Code metadata tables (`SYS_CD_BAS`, `SYS_CD_GROUP_BAS`):

1. **Table Names**: Must be strictly uppercase (e.g., `SYS_CD_BAS`, `SYS_CD_GROUP_BAS`).
2. **Column Names**: Must be strictly uppercase (e.g., `SYS_GROUP_ID`, `SYS_CD_ID`, `SYS_CD_NM`, `CRT_DT`, `UPD_DT`, `DESC_TXT`, `REF_VAL_1`).
3. **Primary Key Data (Codes)**: All actual codes and group IDs inserted into the database must be entirely uppercase (e.g., `VIEW_LIST`, `AWS`, `GPU_PROVIDER`).

Do NOT use lowercase or camelCase for these specific metadata tables in SQLAlchemy definitions or raw SQL.
