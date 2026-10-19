const TICKS = [0, 1, 2, 3, 4, 5, 6, 7, 8]

export function ComputePlot() {
  return (
    <svg
      aria-hidden="true"
      viewBox="0 0 320 72"
      className="compute-plot h-auto w-full max-w-xl text-primary"
      fill="none"
      stroke="currentColor"
    >
      <g className="cp-frame" strokeWidth="1">
        <path d="M8 4 V64 H312" pathLength={1} />
        {TICKS.map((tick) => (
          <path key={tick} d={`M${8 + tick * 38} 64 v4`} pathLength={1} />
        ))}
      </g>
      <path
        className="cp-curve"
        d="M8 60 L46 54 L84 45 L122 36 L160 29 L198 23 L236 19 L274 16 L312 14"
        strokeWidth="3"
        pathLength={1}
       
      />
      <g className="cp-mark" strokeWidth="1">
        <path d="M236 4 V64 M8 19 H312" strokeDasharray="3 3" />
        <rect x="229" y="12" width="14" height="14" fill="currentColor" />
      </g>
    </svg>
  )
}
