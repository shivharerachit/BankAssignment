# Bank Assignment API

This project is created using **Flask** (A framework of Python). Time taken to create and host this project is approximately **4 hours**.

## 🌐 Hosted API
**Base URL:** https://bankassignment.onrender.com/

## 📋 API Endpoints

### 1. Get Branch by IFSC Code

- **Endpoint:** `/api/branches/{IFSC-code}`
- **Method:** `GET`
- **Description:** Get details of bank branch with a specific IFSC code

#### Example Request:
```
GET /api/branches/SBIN0000166
```

#### Example Response:
```json
[
    {
        "address": "S.V.SARANI, RANAGHAT, 24 PGS N, W.B-741201",
        "bank_id": 1,
        "bank_name": "STATE BANK OF INDIA",
        "branch": "RANAGHAT",
        "city": "RANAGHAT",
        "district": "NADIA",
        "ifsc": "SBIN0000166",
        "state": "WEST BENGAL"
    }
]
```

### 2. Get All Banks

- **Endpoint:** `/api/banks`
- **Method:** `GET`
- **Description:** Get list of all banks

#### Example Response:
```json
[
    {
        "id": 1,
        "name": "STATE BANK OF INDIA"
    },
    {
        "id": 2,
        "name": "PUNJAB NATIONAL BANK"
    },
    {
        "id": 3,
        "name": "CANARA BANK"
    }
]
```

### 3. Get Branches by Bank ID

- **Endpoint:** `/api/banks/{bank_id}/branches`
- **Method:** `GET`
- **Description:** Get list of all branches for a specific bank

#### Example Request:
```
GET /api/banks/1/branches
```

#### Example Response:
```json
[
    {
        "address": "CHEGUNTA",
        "bank_id": 1,
        "bank_name": "STATE BANK OF INDIA",
        "branch": "CHEGUNTA",
        "city": "CHEGUNTA",
        "district": "MEDAK",
        "ifsc": "SBIN0004722",
        "state": "ANDHRA PRADESH"
    },
    {
        "address": "BILARI LUCKNOW",
        "bank_id": 1,
        "bank_name": "STATE BANK OF INDIA",
        "branch": "BILARI",
        "city": "BILARI",
        "district": "MORADABAD",
        "ifsc": "SBIN0000595",
        "state": "UTTAR PRADESH"
    },
    {
        "address": "DISTBUXAR  BIHAR 802101",
        "bank_id": 1,
        "bank_name": "STATE BANK OF INDIA",
        "branch": "MAIN ROAD BUXAR",
        "city": "BUXAR",
        "district": "BUXAR",
        "ifsc": "SBIN0001227",
        "state": "BIHAR"
    }
]
```