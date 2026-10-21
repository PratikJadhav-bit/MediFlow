"""
MediFlow AI — Database Seeding Script
Populates the SQLite database with realistic sample data
"""
from datetime import date, datetime, timedelta
import random
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.models import (
    Medicine, Patient, Prescription, PrescriptionItem,
    Order, OrderItem, Branch, DrugInteraction, Reminder,
    Delivery, RestockOrder, SalesRecord
)

_seeded = False


def seed_database():
    """Idempotent seed — only runs once per process."""
    global _seeded
    if _seeded:
        return
    _seeded = True

    db = SessionLocal()
    try:
        if db.query(Medicine).count() > 0:
            return  # Already seeded
        _seed_all(db)
        print("✅ Database seeded successfully")
    except Exception as e:
        db.rollback()
        print(f"❌ Seeding error: {e}")
    finally:
        db.close()


def _seed_all(db: Session):
    # ── Branches ──────────────────────────────────────────────
    branches = [
        Branch(branch_code="BR-01", name="MediFlow Central", location="Connaught Place, New Delhi",
               manager="Dr. Pratik Kumar", phone="+91 11 2345 6789", is_main=True,
               status="active", monthly_revenue=284500, staff_count=12),
        Branch(branch_code="BR-02", name="MediFlow East", location="Lajpat Nagar, New Delhi",
               manager="Anita Singh", phone="+91 11 2345 6790", is_main=False,
               status="active", monthly_revenue=156800, staff_count=8),
        Branch(branch_code="BR-03", name="MediFlow West", location="Dwarka, New Delhi",
               manager="Rajan Malhotra", phone="+91 11 2345 6791", is_main=False,
               status="active", monthly_revenue=198200, staff_count=10),
        Branch(branch_code="BR-04", name="MediFlow North", location="Rohini, New Delhi",
               manager="Sunita Patel", phone="+91 11 2345 6792", is_main=False,
               status="warning", monthly_revenue=132600, staff_count=7),
        Branch(branch_code="BR-05", name="MediFlow South", location="Saket, New Delhi",
               manager="Kiran Sharma", phone="+91 11 2345 6793", is_main=False,
               status="active", monthly_revenue=212000, staff_count=9),
    ]
    db.add_all(branches)
    db.flush()

    # ── Medicines ──────────────────────────────────────────────
    today = date.today()
    meds_data = [
        dict(code="M001", name="Paracetamol 500mg", generic_name="Acetaminophen",
             category="Analgesic", manufacturer="Sun Pharma", hsn_code="30049099",
             location="A-01", unit="tablet", mrp=12.50, cost_price=6.00,
             stock_qty=842, min_stock=100, max_stock=1000, reorder_qty=300,
             expiry_date=today + timedelta(days=400), requires_prescription=False),
        dict(code="M002", name="Amoxicillin 250mg", generic_name="Amoxicillin",
             category="Antibiotic", manufacturer="Cipla", hsn_code="30041090",
             location="B-03", unit="capsule", mrp=48.00, cost_price=24.00,
             stock_qty=42, min_stock=80, max_stock=500, reorder_qty=200,
             expiry_date=today + timedelta(days=7), requires_prescription=True),
        dict(code="M003", name="Metformin 500mg", generic_name="Metformin HCl",
             category="Antidiabetic", manufacturer="Dr. Reddy's", hsn_code="30049099",
             location="C-02", unit="tablet", mrp=35.00, cost_price=16.00,
             stock_qty=310, min_stock=150, max_stock=600, reorder_qty=200,
             expiry_date=today + timedelta(days=450), requires_prescription=True),
        dict(code="M004", name="Atorvastatin 10mg", generic_name="Atorvastatin Calcium",
             category="Statin", manufacturer="Pfizer", hsn_code="30049099",
             location="D-04", unit="tablet", mrp=65.00, cost_price=30.00,
             stock_qty=185, min_stock=60, max_stock=400, reorder_qty=150,
             expiry_date=today + timedelta(days=530), requires_prescription=True),
        dict(code="M005", name="Insulin Glargine 100IU", generic_name="Insulin Glargine",
             category="Insulin", manufacturer="Novo Nordisk", hsn_code="30043900",
             location="REF-01", unit="vial", mrp=890.00, cost_price=420.00,
             stock_qty=5, min_stock=20, max_stock=100, reorder_qty=30,
             expiry_date=today + timedelta(days=220), requires_prescription=True,
             is_refrigerated=True, is_emergency=True),
        dict(code="M006", name="Omeprazole 20mg", generic_name="Omeprazole",
             category="PPI", manufacturer="Ranbaxy", hsn_code="30049099",
             location="A-05", unit="capsule", mrp=28.00, cost_price=12.00,
             stock_qty=420, min_stock=100, max_stock=800, reorder_qty=250,
             expiry_date=today + timedelta(days=360), requires_prescription=False),
        dict(code="M007", name="Azithromycin 500mg", generic_name="Azithromycin",
             category="Antibiotic", manufacturer="Cipla", hsn_code="30041090",
             location="B-06", unit="tablet", mrp=95.00, cost_price=45.00,
             stock_qty=68, min_stock=50, max_stock=300, reorder_qty=120,
             expiry_date=today + timedelta(days=45), requires_prescription=True),
        dict(code="M008", name="Losartan 50mg", generic_name="Losartan Potassium",
             category="ARB/Antihypertensive", manufacturer="Lupin", hsn_code="30049099",
             location="C-07", unit="tablet", mrp=55.00, cost_price=25.00,
             stock_qty=245, min_stock=80, max_stock=500, reorder_qty=180,
             expiry_date=today + timedelta(days=620), requires_prescription=True),
        dict(code="M009", name="Cetirizine 10mg", generic_name="Cetirizine HCl",
             category="Antihistamine", manufacturer="Sun Pharma", hsn_code="30049099",
             location="A-08", unit="tablet", mrp=18.00, cost_price=7.00,
             stock_qty=635, min_stock=120, max_stock=1000, reorder_qty=300,
             expiry_date=today + timedelta(days=480), requires_prescription=False),
        dict(code="M010", name="Amlodipine 5mg", generic_name="Amlodipine Besylate",
             category="CCB/Antihypertensive", manufacturer="Pfizer", hsn_code="30049099",
             location="D-09", unit="tablet", mrp=42.00, cost_price=19.00,
             stock_qty=167, min_stock=70, max_stock=400, reorder_qty=150,
             expiry_date=today + timedelta(days=390), requires_prescription=True),
        dict(code="M011", name="Pantoprazole 40mg", generic_name="Pantoprazole Sodium",
             category="PPI", manufacturer="Torrent", hsn_code="30049099",
             location="A-10", unit="tablet", mrp=32.00, cost_price=14.00,
             stock_qty=88, min_stock=80, max_stock=400, reorder_qty=150,
             expiry_date=today + timedelta(days=4), requires_prescription=False),
        dict(code="M012", name="Montelukast 10mg", generic_name="Montelukast Sodium",
             category="Leukotriene Antagonist", manufacturer="Glenmark", hsn_code="30049099",
             location="E-02", unit="tablet", mrp=78.00, cost_price=36.00,
             stock_qty=198, min_stock=60, max_stock=350, reorder_qty=120,
             expiry_date=today + timedelta(days=560), requires_prescription=True),
        dict(code="M013", name="Epinephrine 1mg/mL", generic_name="Adrenaline",
             category="Emergency", manufacturer="Hameln", hsn_code="30043900",
             location="EMRG-A", unit="ampoule", mrp=145.00, cost_price=72.00,
             stock_qty=8, min_stock=10, max_stock=50, reorder_qty=20,
             expiry_date=today + timedelta(days=240), requires_prescription=True,
             is_emergency=True),
        dict(code="M014", name="Glyceryl Trinitrate 0.5mg", generic_name="Nitroglycerin",
             category="Emergency/Cardiac", manufacturer="Samarth", hsn_code="30049099",
             location="EMRG-B", unit="tablet", mrp=62.00, cost_price=28.00,
             stock_qty=3, min_stock=8, max_stock=40, reorder_qty=15,
             expiry_date=today + timedelta(days=105), requires_prescription=True,
             is_emergency=True, is_controlled=True),
        dict(code="M015", name="Diazepam 10mg", generic_name="Diazepam",
             category="Emergency/Anxiolytic", manufacturer="Roche", hsn_code="30049099",
             location="CTRL-A", unit="tablet", mrp=38.00, cost_price=18.00,
             stock_qty=6, min_stock=10, max_stock=30, reorder_qty=15,
             expiry_date=today + timedelta(days=280), requires_prescription=True,
             is_emergency=True, is_controlled=True),
    ]
    medicines = [Medicine(**d) for d in meds_data]
    db.add_all(medicines)
    db.flush()

    # ── Patients ───────────────────────────────────────────────
    patients_data = [
        dict(patient_code="P001", name="Ananya Sharma", age=34, gender="Female",
             phone="+91 98765 43210", email="ananya.sharma@email.com",
             blood_group="A+", conditions='["Hypertension","Diabetes Type 2"]',
             allergies='["Penicillin"]'),
        dict(patient_code="P002", name="Rajesh Kumar", age=58, gender="Male",
             phone="+91 87654 32109", email="rajesh.kumar@email.com",
             blood_group="O+", conditions='["Cardiac Disease","Hypercholesterolemia"]',
             allergies='[]'),
        dict(patient_code="P003", name="Priya Nair", age=27, gender="Female",
             phone="+91 76543 21098", email="priya.nair@email.com",
             blood_group="B-", conditions='["Asthma","Seasonal Allergies"]',
             allergies='["Sulfonamides"]'),
        dict(patient_code="P004", name="Mohammed Ali", age=45, gender="Male",
             phone="+91 65432 10987", email="m.ali@email.com",
             blood_group="AB+", conditions='["Diabetes Type 2"]',
             allergies='[]'),
        dict(patient_code="P005", name="Deepa Menon", age=62, gender="Female",
             phone="+91 54321 09876", email="deepa.menon@email.com",
             blood_group="O-", conditions='["Osteoporosis","Hypothyroidism","Acid Reflux"]',
             allergies='["Aspirin","NSAIDs"]'),
        dict(patient_code="P006", name="Vikram Singh", age=39, gender="Male",
             phone="+91 43210 98765", email="vikram.singh@email.com",
             blood_group="A-", conditions='["GERD"]',
             allergies='[]'),
    ]
    patients = [Patient(**d) for d in patients_data]
    db.add_all(patients)
    db.flush()

    # ── Prescriptions ──────────────────────────────────────────
    rx_list = [
        Prescription(rx_number="RX-2026-001", patient_id=patients[0].id,
                     doctor_name="Dr. Ramesh Mehta", doctor_reg="MCI-12345",
                     hospital="Apollo Hospitals", status="pending",
                     prescribed_date=today - timedelta(days=2)),
        Prescription(rx_number="RX-2026-002", patient_id=patients[1].id,
                     doctor_name="Dr. Kavitha Rao", doctor_reg="MCI-23456",
                     hospital="Fortis Healthcare", status="dispensed",
                     prescribed_date=today - timedelta(days=3),
                     dispensed_date=today - timedelta(days=2)),
        Prescription(rx_number="RX-2026-003", patient_id=patients[2].id,
                     doctor_name="Dr. Suresh Pillai", doctor_reg="MCI-34567",
                     hospital="Max Hospital", status="pending",
                     prescribed_date=today - timedelta(days=1)),
        Prescription(rx_number="RX-2026-004", patient_id=patients[3].id,
                     doctor_name="Dr. Fatima Sheikh", doctor_reg="MCI-45678",
                     hospital="Medanta Hospital", status="dispensed",
                     prescribed_date=today - timedelta(days=5),
                     dispensed_date=today - timedelta(days=4)),
    ]
    db.add_all(rx_list)
    db.flush()

    # Prescription items
    px_items = [
        PrescriptionItem(prescription_id=rx_list[0].id, medicine_id=medicines[2].id,
                         dosage="1-0-1", duration_days=30, quantity=60),
        PrescriptionItem(prescription_id=rx_list[0].id, medicine_id=medicines[7].id,
                         dosage="0-0-1", duration_days=30, quantity=30),
        PrescriptionItem(prescription_id=rx_list[1].id, medicine_id=medicines[3].id,
                         dosage="0-0-1", duration_days=30, quantity=30),
        PrescriptionItem(prescription_id=rx_list[1].id, medicine_id=medicines[9].id,
                         dosage="1-0-0", duration_days=30, quantity=30),
        PrescriptionItem(prescription_id=rx_list[2].id, medicine_id=medicines[11].id,
                         dosage="0-0-1", duration_days=14, quantity=14),
        PrescriptionItem(prescription_id=rx_list[2].id, medicine_id=medicines[8].id,
                         dosage="0-0-1", duration_days=7, quantity=7),
    ]
    db.add_all(px_items)
    db.flush()

    # ── Orders ─────────────────────────────────────────────────
    order_statuses = ["new", "packing", "ready", "delivered", "delivered",
                      "delivered", "delivered", "new", "packing", "ready"]
    orders_list = []
    for i, (pat, status) in enumerate(zip(
        [patients[0], patients[1], patients[2], patients[3], patients[2],
         patients[3], patients[4], patients[5], patients[0], patients[1]],
        order_statuses
    )):
        total = random.uniform(80, 950)
        o = Order(
            order_number=f"ORD-{5510+i+1}",
            patient_id=pat.id,
            branch_id=branches[0].id,
            status=status,
            order_type=random.choice(["delivery", "pickup"]),
            subtotal=round(total * 0.87, 2),
            discount=round(total * 0.05, 2),
            tax=round(total * 0.08, 2),
            total=round(total, 2),
            payment_method=random.choice(["cash", "card", "upi"]),
            is_paid=status in ["delivered"],
            created_at=datetime.now() - timedelta(minutes=random.randint(2, 180)),
        )
        orders_list.append(o)
    db.add_all(orders_list)
    db.flush()

    # ── Drug Interactions ──────────────────────────────────────
    interactions = [
        DrugInteraction(drug1="Metformin", drug2="Alcohol", severity="moderate",
            description="Alcohol increases the risk of lactic acidosis with Metformin. Concurrent use may also cause hypoglycemia.",
            recommendation="Advise patient to avoid alcohol consumption during Metformin therapy. Monitor blood glucose and lactate levels.",
            mechanism="Alcohol inhibits hepatic gluconeogenesis and increases lactate production, compounding Metformin's effects."),
        DrugInteraction(drug1="Warfarin", drug2="Aspirin", severity="severe",
            description="Concurrent use significantly increases bleeding risk through additive anticoagulant/antiplatelet effects.",
            recommendation="Avoid combination. If necessary, use minimum effective aspirin dose under close physician supervision with INR monitoring.",
            mechanism="Warfarin inhibits vitamin K-dependent clotting factors; aspirin inhibits platelet aggregation and COX-1."),
        DrugInteraction(drug1="Atorvastatin", drug2="Clarithromycin", severity="moderate",
            description="Clarithromycin inhibits CYP3A4 which is responsible for Atorvastatin metabolism, leading to increased statin plasma levels.",
            recommendation="Temporarily suspend statin or use a lower dose. Monitor for signs of myopathy (muscle pain, weakness).",
            mechanism="CYP3A4 inhibition by macrolide antibiotic increases AUC of atorvastatin by up to 80%."),
        DrugInteraction(drug1="Losartan", drug2="Potassium Supplements", severity="mild",
            description="ARBs can cause hyperkalemia. Co-administration with potassium supplements may exacerbate hyperkalemia.",
            recommendation="Monitor serum potassium levels regularly. Adjust supplement dose accordingly.",
            mechanism="Both agents increase serum potassium — ARBs by blocking aldosterone effects; supplements by direct K+ addition."),
        DrugInteraction(drug1="Cetirizine", drug2="Alcohol", severity="mild",
            description="Additive CNS depression. Drowsiness and impaired coordination may be enhanced.",
            recommendation="Advise patient to avoid alcohol and activities requiring full mental alertness (driving, machinery).",
            mechanism="Both agents act as CNS depressants through different mechanisms, with additive sedative effects."),
        DrugInteraction(drug1="Metformin", drug2="IV Contrast Dye", severity="severe",
            description="IV contrast dye can cause acute kidney injury, leading to Metformin accumulation and severe lactic acidosis.",
            recommendation="Stop Metformin 48 hours before contrast procedures. Restart only after confirming normal renal function.",
            mechanism="Contrast nephropathy → reduced GFR → Metformin accumulation → lactic acidosis risk."),
        DrugInteraction(drug1="Amlodipine", drug2="Simvastatin", severity="moderate",
            description="Amlodipine inhibits CYP3A4, increasing simvastatin exposure by approximately 77%.",
            recommendation="Limit simvastatin dose to 20mg daily when co-administered with amlodipine.",
            mechanism="CYP3A4 inhibition by amlodipine impairs first-pass metabolism of simvastatin."),
        DrugInteraction(drug1="Aspirin", drug2="Ibuprofen", severity="moderate",
            description="Ibuprofen may competitively inhibit aspirin's irreversible platelet COX-1 binding, reducing cardioprotective effect.",
            recommendation="If both required, administer aspirin at least 2 hours before ibuprofen. Consider alternative NSAID.",
            mechanism="Competitive COX-1 binding site occupancy by ibuprofen blocks aspirin's acetylation of platelet COX-1."),
    ]
    db.add_all(interactions)

    # ── Reminders ──────────────────────────────────────────────
    reminders = [
        Reminder(patient_id=patients[0].id, medicine_name="Metformin 500mg",
                 reminder_time="08:00", frequency="daily", is_active=True,
                 message_template="Good morning! Time to take your Metformin 500mg. Stay healthy! 💊"),
        Reminder(patient_id=patients[1].id, medicine_name="Atorvastatin 10mg",
                 reminder_time="21:00", frequency="daily", is_active=True,
                 message_template="Good evening! Your Atorvastatin 10mg is due. Take with water. 🌙"),
        Reminder(patient_id=patients[3].id, medicine_name="Insulin Glargine",
                 reminder_time="22:00", frequency="daily", is_active=True,
                 message_template="Reminder: Insulin Glargine at bedtime. Check your blood sugar first. 💉"),
        Reminder(patient_id=patients[2].id, medicine_name="Montelukast 10mg",
                 reminder_time="21:00", frequency="daily", is_active=False,
                 message_template="Time for your Montelukast 10mg. Take at night for best effect. 🌛"),
        Reminder(patient_id=patients[4].id, medicine_name="Omeprazole 20mg",
                 reminder_time="07:30", frequency="daily", is_active=True,
                 message_template="Morning reminder: Omeprazole 20mg before breakfast. 🌅"),
    ]
    db.add_all(reminders)

    # ── Deliveries ──────────────────────────────────────────────
    active_orders = [o for o in orders_list if o.status in ["new", "packing", "ready"]]
    delivery_agents = ["Ravi Kumar", "Pradeep Yadav", "Mohan Das"]
    for i, order in enumerate(active_orders[:3]):
        d = Delivery(
            order_id=order.id,
            delivery_agent=delivery_agents[i % len(delivery_agents)],
            agent_phone=f"+91 9876{i}43210",
            status="in_transit",
            current_step=i,
            estimated_mins=random.randint(10, 50),
        )
        db.add(d)

    # ── Sales Records (last 12 months) ─────────────────────────
    categories = ["Antibiotics", "Analgesics", "Antidiabetics", "Cardiovascular", "Antihistamines", "Others"]
    for month_offset in range(12):
        rec_date = today.replace(day=1) - timedelta(days=month_offset * 30)
        base_rev = 150000 + month_offset * 5000 + random.randint(-10000, 15000)
        for cat in categories:
            cat_rev = base_rev * random.uniform(0.1, 0.25)
            db.add(SalesRecord(
                date=rec_date,
                branch_id=branches[0].id,
                category=cat,
                revenue=round(cat_rev, 2),
                orders_count=random.randint(80, 350),
                units_sold=random.randint(200, 1200),
            ))

    # ── Restock Orders ──────────────────────────────────────────
    for med in medicines:
        if med.stock_qty < med.min_stock:
            db.add(RestockOrder(
                medicine_id=med.id,
                supplier="MedSupply India Pvt Ltd",
                quantity=med.reorder_qty,
                unit_cost=round(med.cost_price * 0.9, 2) if med.cost_price else 0,
                total_cost=round((med.cost_price or 0) * 0.9 * med.reorder_qty, 2),
                status="pending",
                ordered_at=datetime.now(),
            ))

    db.commit()
