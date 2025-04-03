const { onSchedule } = require('firebase-functions/v2/scheduler');
const admin = require('firebase-admin');
require('dotenv').config();
const fetch = (...args) => import('node-fetch').then(({ default: fetch }) => fetch(...args));

admin.initializeApp();
const db = admin.firestore();

exports.sendReminderEmails = onSchedule('every 24 hours', async () => {
  const today = new Date();

  // ✅ Production: look ahead 14 days
  const reminderDate = new Date(today.setDate(today.getDate() + 14));

  const year = reminderDate.getFullYear();
  const month = String(reminderDate.getMonth() + 1).padStart(2, '0');
  const day = String(reminderDate.getDate()).padStart(2, '0');
  const formattedDate = `${year}-${month}-${day}`;

  console.log(`📅 Looking for events on: ${formattedDate}`);

  try {
    const snapshot = await db.collection('contracts')
      .where('eventDate', '==', formattedDate)
      .get();

    if (snapshot.empty) {
      console.log('No reminders to send today.');
      return;
    }

    for (const doc of snapshot.docs) {
      const data = doc.data();

      // ✅ Skip if already sent
      if (data.reminderSent) {
        console.log(`⏭ Already sent to ${data.email}, skipping.`);
        continue;
      }

      // ✅ Send the reminder email via EmailJS REST API
      await fetch('https://api.emailjs.com/api/v1.0/email/send', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${process.env.EMAILJS_PRIVATE_KEY}`
        },
        body: JSON.stringify({
          service_id: process.env.EMAILJS_SERVICE_ID,
          template_id: process.env.EMAILJS_REMINDER_TEMPLATE_ID,
          template_params: {
            client_name: data.clientName,
            client_email: data.email,
            event_date: data.eventDate,
            event_type: data.eventType,
            total_due: `$${calculateTotal(data)}`
          }
        })
      });

      // ✅ Mark reminder as sent
      await db.collection('contracts').doc(doc.id).update({
        reminderSent: true
      });

      console.log(`✅ Reminder sent to ${data.email}`);
    }
  } catch (err) {
    console.error('❌ Error checking contracts or sending reminders:', err);
  }
});

function calculateTotal(data) {
  let total = 350;
  if (data.lighting) total += 100;
  if (data.photography) total += 150;
  if (data.videoVisuals) total += 100;
  if (data.additionalHours) total += data.additionalHours * 75;
  return total;
}
