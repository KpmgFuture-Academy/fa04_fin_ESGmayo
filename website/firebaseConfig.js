// firebaseConfig.js
import { initializeApp } from "firebase/app";
import { getFirestore } from "firebase/firestore";  // Firestore용

const firebaseConfig = {
  apiKey: "AIzaSyBN965sQRm-wSAKpewEQIYSabo_C4iFMak",
  authDomain: "esgmayo-34ad9.firebaseapp.com",
  projectId: "esgmayo-34ad9",
  storageBucket: "esgmayo-34ad9.firebasestorage.app",
  messagingSenderId: "965037628249",
  appId: "1:965037628249:web:2684a1fec4fa8b0009ca48"
};

// Firebase 앱 초기화
const app = initializeApp(firebaseConfig);

// Firestore DB 가져오기
const db = getFirestore(app);

// 필요한 경우 export
export { db };
