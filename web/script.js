function loadDashboard() {
    const dashboardContent = document.getElementById('dashboard-content');
    dashboardContent.innerHTML = `
        <p><strong>통합 리스크:</strong> 재무, ESG, 기업, 산업 데이터 분석 결과</p>
        <p><strong>유사기업 비교:</strong> 산업, 매출, ESG 점수 기반 클러스터링</p>
        <p><strong>그린워싱 경고:</strong> 리포트 감정 분석 결과</p>
    `;
    alert('대시보드가 새로고침되었습니다!');
}

function uploadFile() {
    const fileInput = document.getElementById('csvFile');
    const file = fileInput.files[0];
    const resultDiv = document.getElementById('analysis-result');

    if (!file) {
        alert('CSV 파일을 선택해주세요!');
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    fetch('/analyze', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        resultDiv.innerHTML = `<p><strong>분석 결과:</strong> ${data.message}</p>`;
    })
    .catch(error => {
        resultDiv.innerHTML = `<p>오류 발생: ${error.message}</p>`;
    });
}

document.addEventListener('DOMContentLoaded', () => {
    loadDashboard();
});
