function loadDashboard() {
    // 대시보드 데이터를 동적으로 로드하는 예시 (API 연동 가능성 시뮬레이션)
    const dashboardContent = document.getElementById('dashboard-content');
    dashboardContent.innerHTML = `
        <p><strong>통합 리스크:</strong> 재무, ESG, 기업, 산업 데이터 분석 결과</p>
        <p><strong>유사기업 비교:</strong> 산업, 매출, ESG 점수 기반 클러스터링</p>
        <p><strong>그린워싱 경고:</strong> 리포트 감정 분석 결과</p>
    `;
    alert('대시보드가 새로고침되었습니다!');
}

// 페이지 로드 시 기본 데이터 표시
document.addEventListener('DOMContentLoaded', () => {
    loadDashboard();
});