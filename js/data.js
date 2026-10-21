// ============================================================
// MediFlow AI — Mock Data Store
// ============================================================

const MEDIFLOW_DATA = {

  // ── Medicines ──────────────────────────────────────────────
  medicines: [
    { id: 'M001', name: 'Paracetamol 500mg', generic: 'Acetaminophen', category: 'Analgesic', stock: 842, minStock: 100, maxStock: 1000, price: 12.50, costPrice: 6.00, expiryDate: '2027-03-15', manufacturer: 'Sun Pharma', location: 'A-01', sold30d: 284, color: 'blue', emoji: '💊', hsn: '30049099' },
    { id: 'M002', name: 'Amoxicillin 250mg', generic: 'Amoxicillin', category: 'Antibiotic', stock: 42, minStock: 80, maxStock: 500, price: 48.00, costPrice: 24.00, expiryDate: '2026-06-02', manufacturer: 'Cipla', location: 'B-03', sold30d: 96, color: 'amber', emoji: '🔴', hsn: '30041090' },
    { id: 'M003', name: 'Metformin 500mg', generic: 'Metformin HCl', category: 'Antidiabetic', stock: 310, minStock: 150, maxStock: 600, price: 35.00, costPrice: 16.00, expiryDate: '2027-08-20', manufacturer: 'Dr. Reddy\'s', location: 'C-02', sold30d: 178, color: 'emerald', emoji: '🩺', hsn: '30049099' },
    { id: 'M004', name: 'Atorvastatin 10mg', generic: 'Atorvastatin Calcium', category: 'Statin', stock: 185, minStock: 60, maxStock: 400, price: 65.00, costPrice: 30.00, expiryDate: '2027-11-10', manufacturer: 'Pfizer', location: 'D-04', sold30d: 112, color: 'violet', emoji: '❤️', hsn: '30049099' },
    { id: 'M005', name: 'Insulin Glargine', generic: 'Insulin Glargine', category: 'Insulin', stock: 5, minStock: 20, maxStock: 100, price: 890.00, costPrice: 420.00, expiryDate: '2026-12-31', manufacturer: 'Novo Nordisk', location: 'REF-01', sold30d: 42, color: 'rose', emoji: '💉', hsn: '30043900' },
    { id: 'M006', name: 'Omeprazole 20mg', generic: 'Omeprazole', category: 'PPI', stock: 420, minStock: 100, maxStock: 800, price: 28.00, costPrice: 12.00, expiryDate: '2027-05-18', manufacturer: 'Ranbaxy', location: 'A-05', sold30d: 198, color: 'sky', emoji: '💙', hsn: '30049099' },
    { id: 'M007', name: 'Azithromycin 500mg', generic: 'Azithromycin', category: 'Antibiotic', stock: 68, minStock: 50, maxStock: 300, price: 95.00, costPrice: 45.00, expiryDate: '2026-07-14', manufacturer: 'Cipla', location: 'B-06', sold30d: 72, color: 'indigo', emoji: '🔵', hsn: '30041090' },
    { id: 'M008', name: 'Losartan 50mg', generic: 'Losartan Potassium', category: 'ARB', stock: 245, minStock: 80, maxStock: 500, price: 55.00, costPrice: 25.00, expiryDate: '2028-01-25', manufacturer: 'Lupin', location: 'C-07', sold30d: 134, color: 'blue', emoji: '🩵', hsn: '30049099' },
    { id: 'M009', name: 'Cetirizine 10mg', generic: 'Cetirizine HCl', category: 'Antihistamine', stock: 635, minStock: 120, maxStock: 1000, price: 18.00, costPrice: 7.00, expiryDate: '2027-09-30', manufacturer: 'Sun Pharma', location: 'A-08', sold30d: 215, color: 'emerald', emoji: '🟢', hsn: '30049099' },
    { id: 'M010', name: 'Amlodipine 5mg', generic: 'Amlodipine Besylate', category: 'CCB', stock: 167, minStock: 70, maxStock: 400, price: 42.00, costPrice: 19.00, expiryDate: '2027-06-15', manufacturer: 'Pfizer', location: 'D-09', sold30d: 98, color: 'amber', emoji: '🟡', hsn: '30049099' },
    { id: 'M011', name: 'Pantoprazole 40mg', generic: 'Pantoprazole Sodium', category: 'PPI', stock: 88, minStock: 80, maxStock: 400, price: 32.00, costPrice: 14.00, expiryDate: '2026-05-30', manufacturer: 'Torrent', location: 'A-10', sold30d: 145, color: 'rose', emoji: '🔴', hsn: '30049099' },
    { id: 'M012', name: 'Montelukast 10mg', generic: 'Montelukast Sodium', category: 'Leukotriene', stock: 198, minStock: 60, maxStock: 350, price: 78.00, costPrice: 36.00, expiryDate: '2027-12-20', manufacturer: 'Glenmark', location: 'E-02', sold30d: 89, color: 'violet', emoji: '🟣', hsn: '30049099' },
  ],

  // ── Patients ───────────────────────────────────────────────
  patients: [
    { id: 'P001', name: 'Ananya Sharma', age: 34, phone: '+91 98765 43210', bloodGroup: 'A+', conditions: ['Hypertension', 'Diabetes'], lastVisit: '2026-05-24', totalOrders: 28 },
    { id: 'P002', name: 'Rajesh Kumar', age: 58, phone: '+91 87654 32109', bloodGroup: 'O+', conditions: ['Cardiac', 'Cholesterol'], lastVisit: '2026-05-23', totalOrders: 42 },
    { id: 'P003', name: 'Priya Nair', age: 27, phone: '+91 76543 21098', bloodGroup: 'B-', conditions: ['Asthma'], lastVisit: '2026-05-22', totalOrders: 15 },
    { id: 'P004', name: 'Mohammed Ali', age: 45, phone: '+91 65432 10987', bloodGroup: 'AB+', conditions: ['Diabetes Type 2'], lastVisit: '2026-05-20', totalOrders: 34 },
    { id: 'P005', name: 'Deepa Menon', age: 62, phone: '+91 54321 09876', bloodGroup: 'O-', conditions: ['Osteoporosis', 'Thyroid'], lastVisit: '2026-05-19', totalOrders: 56 },
    { id: 'P006', name: 'Vikram Singh', age: 39, phone: '+91 43210 98765', bloodGroup: 'A-', conditions: ['Acid Reflux'], lastVisit: '2026-05-18', totalOrders: 12 },
  ],

  // ── Prescriptions ──────────────────────────────────────────
  prescriptions: [
    { id: 'RX-2024-001', patientId: 'P001', patient: 'Ananya Sharma', doctor: 'Dr. Ramesh Mehta', date: '2026-05-24', status: 'pending', medicines: [{ name: 'Metformin 500mg', dose: '1-0-1', days: 30 }, { name: 'Losartan 50mg', dose: '0-0-1', days: 30 }] },
    { id: 'RX-2024-002', patientId: 'P002', patient: 'Rajesh Kumar', doctor: 'Dr. Kavitha Rao', date: '2026-05-23', status: 'dispensed', medicines: [{ name: 'Atorvastatin 10mg', dose: '0-0-1', days: 30 }, { name: 'Amlodipine 5mg', dose: '1-0-0', days: 30 }] },
    { id: 'RX-2024-003', patientId: 'P003', patient: 'Priya Nair', doctor: 'Dr. Suresh Pillai', date: '2026-05-22', status: 'pending', medicines: [{ name: 'Montelukast 10mg', dose: '0-0-1', days: 14 }, { name: 'Cetirizine 10mg', dose: '0-0-1', days: 7 }] },
    { id: 'RX-2024-004', patientId: 'P004', patient: 'Mohammed Ali', doctor: 'Dr. Fatima Sheikh', date: '2026-05-20', status: 'dispensed', medicines: [{ name: 'Insulin Glargine', dose: '14 units at bedtime', days: 30 }, { name: 'Metformin 500mg', dose: '1-1-1', days: 30 }] },
    { id: 'RX-2024-005', patientId: 'P005', patient: 'Deepa Menon', doctor: 'Dr. Ramesh Mehta', date: '2026-05-19', status: 'dispensed', medicines: [{ name: 'Omeprazole 20mg', dose: '1-0-0', days: 14 }] },
  ],

  // ── Orders ─────────────────────────────────────────────────
  orders: [
    { id: 'ORD-5521', patient: 'Ananya Sharma', items: 3, amount: 287.50, status: 'new', time: '2 min ago', type: 'delivery' },
    { id: 'ORD-5520', patient: 'Rajesh Kumar', items: 2, amount: 152.00, status: 'packing', time: '8 min ago', type: 'pickup' },
    { id: 'ORD-5519', patient: 'Meera Joshi', items: 5, amount: 643.00, status: 'ready', time: '15 min ago', type: 'delivery' },
    { id: 'ORD-5518', patient: 'Suresh Patel', items: 1, amount: 89.00, status: 'delivered', time: '32 min ago', type: 'pickup' },
    { id: 'ORD-5517', patient: 'Priya Nair', items: 4, amount: 312.00, status: 'delivered', time: '1h ago', type: 'delivery' },
    { id: 'ORD-5516', patient: 'Mohammed Ali', items: 2, amount: 925.00, status: 'delivered', time: '2h ago', type: 'delivery' },
    { id: 'ORD-5515', patient: 'Deepa Menon', items: 3, amount: 168.00, status: 'delivered', time: '3h ago', type: 'pickup' },
    { id: 'ORD-5514', patient: 'Vikram Singh', items: 2, amount: 95.00, status: 'new', time: '4 min ago', type: 'delivery' },
    { id: 'ORD-5513', patient: 'Kavya Reddy', items: 6, amount: 540.00, status: 'packing', time: '11 min ago', type: 'delivery' },
    { id: 'ORD-5512', patient: 'Arjun Verma', items: 1, amount: 48.00, status: 'ready', time: '25 min ago', type: 'pickup' },
  ],

  // ── Branches ───────────────────────────────────────────────
  branches: [
    { id: 'BR-01', name: 'MediFlow Central', location: 'Connaught Place, Delhi', manager: 'Dr. Pratik Kumar', revenue: 284500, orders: 1240, stock: 98, status: 'active', isMain: true, staff: 12 },
    { id: 'BR-02', name: 'MediFlow East', location: 'Lajpat Nagar, Delhi', manager: 'Anita Singh', revenue: 156800, orders: 820, stock: 73, status: 'active', isMain: false, staff: 8 },
    { id: 'BR-03', name: 'MediFlow West', location: 'Dwarka, Delhi', manager: 'Rajan Malhotra', revenue: 198200, orders: 945, stock: 91, status: 'active', isMain: false, staff: 10 },
    { id: 'BR-04', name: 'MediFlow North', location: 'Rohini, Delhi', manager: 'Sunita Patel', revenue: 132600, orders: 680, stock: 65, status: 'warning', isMain: false, staff: 7 },
    { id: 'BR-05', name: 'MediFlow South', location: 'Saket, Delhi', manager: 'Kiran Sharma', revenue: 212000, orders: 1050, stock: 88, status: 'active', isMain: false, staff: 9 },
  ],

  // ── Drug Interactions DB ────────────────────────────────────
  interactions: {
    'metformin+alcohol': { severity: 'moderate', desc: 'Alcohol increases the risk of lactic acidosis with metformin. Advise patient to avoid alcohol.', recommendation: 'Monitor closely. Advise patient to limit alcohol intake.' },
    'warfarin+aspirin': { severity: 'severe', desc: 'Combination significantly increases bleeding risk. Both drugs inhibit clotting through different mechanisms.', recommendation: 'Avoid combination if possible. Use with extreme caution under physician supervision.' },
    'metformin+contrast': { severity: 'severe', desc: 'IV contrast dye can cause acute kidney injury, increasing metformin accumulation and risk of lactic acidosis.', recommendation: 'Stop metformin 48h before contrast procedure. Restart only after confirming normal renal function.' },
    'atorvastatin+clarithromycin': { severity: 'moderate', desc: 'Clarithromycin inhibits CYP3A4 which metabolizes atorvastatin, leading to increased statin levels and risk of myopathy.', recommendation: 'Temporarily suspend statin or use lower dose. Monitor for muscle pain.' },
    'losartan+potassium': { severity: 'mild', desc: 'ARBs can cause hyperkalemia. Combining with potassium supplements may exacerbate this.', recommendation: 'Monitor serum potassium levels regularly.' },
    'cetirizine+alcohol': { severity: 'mild', desc: 'Additive CNS depression. Drowsiness may be enhanced.', recommendation: 'Advise patient to avoid alcohol and activities requiring mental alertness.' },
  },

  // ── Sales Data ─────────────────────────────────────────────
  salesMonthly: [182000, 195000, 221000, 208000, 245000, 268000, 242000, 289000, 312000, 298000, 334000, 356000],
  salesWeekly:  [48000, 52000, 61000, 57000, 65000, 72000, 69000],

  // ── Category Distribution ──────────────────────────────────
  categoryData: {
    labels: ['Antibiotics', 'Analgesics', 'Antidiabetics', 'Cardiovascular', 'Antihistamines', 'Others'],
    values: [22, 18, 16, 14, 12, 18],
  },

  // ── Demand Forecast ────────────────────────────────────────
  forecastData: {
    labels: ['Jun 1', 'Jun 7', 'Jun 14', 'Jun 21', 'Jun 28', 'Jul 5', 'Jul 12'],
    actual:    [820, 945, 780, 1020, 890, null, null],
    predicted: [820, 945, 780, 1020, 890, 1150, 1240],
    lower:     [780, 890, 720, 950, 820, 1050, 1100],
    upper:     [860, 1010, 840, 1090, 960, 1250, 1380],
  },

  // ── WhatsApp Reminders ─────────────────────────────────────
  reminders: [
    { id: 'R001', patient: 'Ananya Sharma', medicine: 'Metformin 500mg', time: '08:00 AM', frequency: 'Daily', nextSend: '2026-05-27 08:00', status: 'active', phone: '+91 98765 43210' },
    { id: 'R002', patient: 'Rajesh Kumar', medicine: 'Atorvastatin 10mg', time: '09:00 PM', frequency: 'Daily', nextSend: '2026-05-26 21:00', status: 'active', phone: '+91 87654 32109' },
    { id: 'R003', patient: 'Mohammed Ali', medicine: 'Insulin Glargine', time: '10:00 PM', frequency: 'Daily', nextSend: '2026-05-26 22:00', status: 'active', phone: '+91 65432 10987' },
    { id: 'R004', patient: 'Priya Nair', medicine: 'Montelukast 10mg', time: '09:00 PM', frequency: 'Daily', nextSend: '2026-05-27 21:00', status: 'paused', phone: '+91 76543 21098' },
    { id: 'R005', patient: 'Deepa Menon', medicine: 'Omeprazole 20mg', time: '07:30 AM', frequency: 'Daily', nextSend: '2026-05-27 07:30', status: 'active', phone: '+91 54321 09876' },
  ],

  // ── Patient History ────────────────────────────────────────
  patientHistory: {
    P001: [
      { date: '2026-05-24', type: 'purchase', items: ['Metformin 500mg x30', 'Losartan 50mg x30'], amount: 2700, prescriptionId: 'RX-2024-001' },
      { date: '2026-04-25', type: 'purchase', items: ['Metformin 500mg x30', 'Losartan 50mg x30'], amount: 2700, prescriptionId: null },
      { date: '2026-03-26', type: 'purchase', items: ['Metformin 500mg x30', 'Cetirizine 10mg x10'], amount: 1230, prescriptionId: null },
      { date: '2026-02-28', type: 'consultation', items: ['BP Check', 'Blood Sugar Test'], amount: 0, prescriptionId: null },
    ],
  },

  // ── Delivery Tracking ──────────────────────────────────────
  activeDeliveries: [
    { id: 'DEL-5519', orderId: 'ORD-5519', patient: 'Meera Joshi', agent: 'Ravi Kumar', step: 2, address: '42, Green Park, New Delhi', eta: '12 min' },
    { id: 'DEL-5521', orderId: 'ORD-5521', patient: 'Ananya Sharma', agent: 'Pradeep Yadav', step: 1, address: '7, Vasant Vihar, New Delhi', eta: '28 min' },
    { id: 'DEL-5514', orderId: 'ORD-5514', patient: 'Vikram Singh', agent: 'Mohan Das', step: 0, address: '15, Defence Colony, New Delhi', eta: '45 min' },
  ],

  // ── Emergency Medicines ────────────────────────────────────
  emergencyMeds: [
    { name: 'Epinephrine (Adrenaline)', stock: 8, minRequired: 10, location: 'Emergency Cabinet A', expiryDate: '2027-01-15', status: 'low' },
    { name: 'Atropine 0.6mg', stock: 15, minRequired: 12, location: 'Emergency Cabinet A', expiryDate: '2027-03-20', status: 'ok' },
    { name: 'Glyceryl Trinitrate', stock: 3, minRequired: 8, location: 'Emergency Cabinet B', expiryDate: '2026-09-10', status: 'critical' },
    { name: 'Furosemide 40mg', stock: 24, minRequired: 15, location: 'Emergency Cabinet B', expiryDate: '2027-06-30', status: 'ok' },
    { name: 'Diazepam 10mg', stock: 6, minRequired: 10, location: 'Controlled Cabinet', expiryDate: '2027-02-28', status: 'low' },
    { name: 'Dextrose 50% IV', stock: 12, minRequired: 10, location: 'Emergency Cabinet C', expiryDate: '2027-08-15', status: 'ok' },
  ],

  // ── AI Recommendations ─────────────────────────────────────
  aiRecommendations: [
    { id: 1, type: 'restock', title: 'Increase Paracetamol Stock Before Monsoon', desc: 'Based on historical data, demand for Paracetamol typically spikes 35% during Jun–Aug due to fever season. Recommend increasing order by 300 units.', tags: ['Seasonal', 'High Priority'], confidence: 94, medicine: 'Paracetamol 500mg', emoji: '📈' },
    { id: 2, type: 'substitute', title: 'Generic Substitute Available: Metformin', desc: 'Glyciphage (Metformin) by Franco-Indian is 40% cheaper than branded equivalent with same bioavailability. Potential monthly savings: ₹4,200.', tags: ['Cost Saving', 'Generic'], confidence: 88, medicine: 'Metformin 500mg', emoji: '💡' },
    { id: 3, type: 'interaction', title: 'Patient Rajesh Kumar - Potential Drug Interaction', desc: 'Patient is prescribed both Atorvastatin and Clarithromycin. CYP3A4 interaction detected. Recommend consultation with prescribing physician.', tags: ['Drug Interaction', 'Urgent'], confidence: 97, medicine: 'Atorvastatin 10mg', emoji: '⚠️' },
    { id: 4, type: 'demand', title: 'Antibiotic Demand Spike Predicted', desc: 'AI model predicts 28% increase in antibiotic demand over next 2 weeks, correlated with seasonal respiratory infection patterns in the region.', tags: ['AI Forecast', 'Demand'], confidence: 82, medicine: 'Azithromycin 500mg', emoji: '🤖' },
    { id: 5, type: 'expiry', title: 'Pantoprazole Near Expiry — Discount Strategy', desc: '88 units of Pantoprazole expire in 4 days. Recommend 15% discount promotion to accelerate sales and minimize waste losses.', tags: ['Expiry Management', 'Revenue'], confidence: 91, medicine: 'Pantoprazole 40mg', emoji: '⏰' },
  ],

  // ── AI Responses (simulated) ───────────────────────────────
  aiResponses: {
    interaction: 'I\'ve analyzed the drug interaction. The combination of **Metformin** and **Alcohol** presents a **moderate** risk of lactic acidosis. I recommend advising the patient to avoid alcohol consumption during treatment. Would you like me to add a reminder alert for this patient?',
    inventory: 'Current inventory status: **842 units** of Paracetamol (84% capacity), **42 units** of Amoxicillin (critical — below minimum stock of 80 units). I\'ve flagged Amoxicillin for urgent restock. Should I generate a purchase order?',
    recommendation: 'Based on the patient\'s age (58), cardiac history, and current medications, I recommend monitoring for drug interactions between **Atorvastatin** and any recently added medications. The AI confidence level for this assessment is **97%**.',
    forecast: 'AI demand forecast for next week shows a **15% spike** in antibiotic demand, likely correlated with seasonal patterns. I recommend pre-ordering 200 units of Azithromycin and 150 units of Amoxicillin to meet projected demand.',
    general: 'I\'m your AI pharmacy assistant powered by MediFlow intelligence. I can help with drug interactions, inventory queries, prescription analysis, demand forecasting, and patient medication history. What would you like to explore?',
  }
};
