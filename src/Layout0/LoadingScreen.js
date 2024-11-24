import React from 'react';
import './LoadingScreen.css'; // 애니메이션과 스타일을 외부 CSS 파일로 관리

const LoadingScreen = () => {
  const techPatternElements = Array.from({ length: 60 }).map((_, i) => (
    <g key={`inner-${i}`} transform={`rotate(${i * 6})`}>
      <rect x="80" y="-1" width="40" height="2" fill="#FFD700" opacity="0.3" />
      <rect x="85" y="-0.5" width="10" height="1" fill="#FFD700" opacity="0.7" />
    </g>
  ));

  const outerTechPatternElements = Array.from({ length: 72 }).map((_, i) => (
    <g key={`outer-${i}`} transform={`rotate(${i * 5})`}>
      <rect
        x="130"
        y="-2"
        width="30"
        height="4"
        fill="url(#techPattern)"
        opacity="0.5"
      />
    </g>
  ));

  return (
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500">
      <defs>
        {/* 발광 그라데이션 */}
        <radialGradient id="centerGlow" cx="50%" cy="50%" r="50%">
          <stop offset="0%" style={{ stopColor: '#FFA500', stopOpacity: 0.7 }} />
          <stop offset="70%" style={{ stopColor: '#FFD700', stopOpacity: 0.2 }} />
          <stop offset="100%" style={{ stopColor: '#FFD700', stopOpacity: 0 }} />
        </radialGradient>
        {/* 기술 패턴용 그라데이션 */}
        <linearGradient id="techPattern" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" style={{ stopColor: '#FFD700', stopOpacity: 0.1 }} />
          <stop offset="50%" style={{ stopColor: '#FFD700', stopOpacity: 0.8 }} />
          <stop offset="100%" style={{ stopColor: '#FFD700', stopOpacity: 0.1 }} />
        </linearGradient>
      </defs>

      {/* 검은 배경 */}
      <rect width="500" height="500" fill="#000000" />

      <g transform="translate(250, 250)">
        {/* 중앙 발광 효과 */}
        <circle
          className="glow-center"
          r="130"
          fill="url(#centerGlow)"
        />

        {/* 기술적 패턴 레이어 */}
        <g className="tech-pattern">
          {techPatternElements}
          {outerTechPatternElements}
        </g>

        {/* 메인 원형 프레임 */}
        <circle
          className="main-circle"
          r="120"
          stroke="#FFD700"
          fill="none"
          strokeWidth="2"
        />
        <circle
          className="main-circle"
          r="140"
          stroke="#FFD700"
          fill="none"
          strokeWidth="1"
          opacity="0.5"
        />

        {/* 중앙 비트코인 로고 */}
        <g className="bitcoin-logo" transform="translate(0, 0) scale(1.5)">
            <text
                x="2"
                y="30"
                fontSize="100"
                //fontWeight="bold"
                textAnchor="middle"
                fill="none" 
                stroke="#FFD700"
                strokeWidth="1"  /* 테두리 두께 조정 */
            >
                B
            </text>
        </g>



        {/* 외부 궤도 요소 */}
        <g className="orbital-elements">
          <circle
            cx="0"
            cy="0"
            r="180"
            stroke="#FFD700"
            strokeWidth="1"
            opacity="0.2"
            fill="none"
          />
          <circle cx="160" cy="0" r="5" fill="#FFD700" />
          <circle cx="-160" cy="0" r="5" fill="#FFD700" />
          <circle cx="0" cy="160" r="5" fill="#FFD700" />
          <circle cx="0" cy="-160" r="5" fill="#FFD700" />
          <circle
            cx="180"
            cy="0"
            r="8"
            fill="none"
            stroke="#FFD700"
            strokeWidth="1"
          />
          <circle
            cx="-180"
            cy="0"
            r="8"
            fill="none"
            stroke="#FFD700"
            strokeWidth="1"
          />
          <circle
            cx="0"
            cy="180"
            r="8"
            fill="none"
            stroke="#FFD700"
            strokeWidth="1"
          />
          <circle
            cx="0"
            cy="-180"
            r="8"
            fill="none"
            stroke="#FFD700"
            strokeWidth="1"
          />
        </g>
      </g>
    </svg>
  );
};

export default LoadingScreen;
