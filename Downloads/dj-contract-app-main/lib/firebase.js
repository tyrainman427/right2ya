// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getFirestore } from 'firebase/firestore';

// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyB2sQum4yspx3e-esifQ8aJsinCQ15gZIA",
  authDomain: "dj-contract-app.firebaseapp.com",
  projectId: "dj-contract-app",
  storageBucket: "dj-contract-app.firebasestorage.app",
  messagingSenderId: "767465862485",
  appId: "1:767465862485:web:40910245f5defe8149ebdc",
  measurementId: "G-XYSZE6FQQC"
};
const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

export default db;