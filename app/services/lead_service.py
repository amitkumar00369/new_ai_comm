import pandas as pd
import os
def create_lead(user_number, entity_type, item_id,tenant_number=None, tenant_id=None):
    lead = {
        "user": user_number,
        "entity_type": entity_type,
        "item_id": item_id,
        "timestamp": pd.Timestamp.now(),
        "tenant_id": tenant_id,
        "tenant_number": tenant_number
    }

    file = "leads.csv"

    if not os.path.exists(file):
        df = pd.DataFrame(columns=["user", "entity_type", "item_id", "timestamp", "tenant_id", "tenant_number"])
    else:
        df = pd.read_csv(file)

    df = pd.concat([df, pd.DataFrame([lead])], ignore_index=True)
    df.to_csv(file, index=False)

    print("Lead Created:", lead)

    return lead