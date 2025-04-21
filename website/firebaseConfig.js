// firebaseConfig.js
import { initializeApp } from "firebase/app";
const firebaseConfig = {
  apiKey: "AIzaSyBN965sQRm-wSAKpewEQIYSabo_C4iFMak",
  authDomain: "esgmayo-34ad9.firebaseapp.com",
  projectId: "esgmayo-34ad9",
  storageBucket: "esgmayo-34ad9.firebasestorage.app",
  messagingSenderId: "965037628249",
  appId: "1:965037628249:web:2684a1fec4fa8b0009ca48"
};

firebase.initializeApp(firebaseConfig);
const db = firebase.firestore(); // 또는 realtime database라면 firebase.database();
