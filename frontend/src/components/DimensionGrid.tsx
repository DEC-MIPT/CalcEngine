const COLUMNS = 12
const ROWS = 8
const CELL = 30

export function DimensionGrid() {
  const width = COLUMNS * CELL
  const height = ROWS * CELL
  return (
    <svg
      aria-hidden="true"
      viewBox={`-20 -20 ${width + 60} ${height + 60}`}
      className="dimension-grid h-auto w-full max-w-md text-primary-foreground"
      fill="none"
      stroke="currentColor"
    >
      <g className="dg-grid" strokeOpacity="0.28" strokeWidth="1" vectorEffect="non-scaling-stroke">
        {Array.from({ length: COLUMNS + 1 }, (_, i) => (
          <line key={`v${i}`} x1={i * CELL} y1={0} x2={i * CELL} y2={height} pathLength={1} />
        ))}
        {Array.from({ length: ROWS + 1 }, (_, i) => (
          <line key={`h${i}`} x1={0} y1={i * CELL} x2={width} y2={i * CELL} pathLength={1} />
        ))}
      </g>
      <g className="dg-ground" strokeWidth="1.5">
        <line x1={0} y1={3 * CELL} x2={width} y2={3 * CELL} pathLength={1} />
      </g>
      <g className="dg-body" strokeWidth="3">
        <path d={`M${4 * CELL} ${3 * CELL} V${6 * CELL} H${8 * CELL} V${3 * CELL}`} pathLength={1} />
        <path d={`M${5.5 * CELL} ${0} V${3 * CELL} M${6.5 * CELL} ${0} V${3 * CELL}`} pathLength={1} />
      </g>
      <g className="dg-dims" strokeWidth="1.5">
        <path
          d={`M${4 * CELL} ${6 * CELL + 6} V${7 * CELL + 10} M${8 * CELL} ${6 * CELL + 6} V${7 * CELL + 10} M${4 * CELL - 10} ${7 * CELL} H${8 * CELL + 10}`}
          pathLength={1}
        />
        <path
          d={`M${4 * CELL - 6} ${7 * CELL + 6} l12 -12 M${8 * CELL - 6} ${7 * CELL + 6} l12 -12`}
          pathLength={1}
        />
        <path
          d={`M${8 * CELL + 6} ${3 * CELL} H${10 * CELL + 10} M${8 * CELL + 6} ${6 * CELL} H${10 * CELL + 10} M${10 * CELL} ${3 * CELL - 10} V${6 * CELL + 10}`}
          pathLength={1}
        />
        <path
          d={`M${10 * CELL - 6} ${3 * CELL + 6} l12 -12 M${10 * CELL - 6} ${6 * CELL + 6} l12 -12`}
          pathLength={1}
        />
        <path d={`M${7 * CELL} ${5 * CELL} L${9.5 * CELL} ${1.5 * CELL} H${11.5 * CELL}`} pathLength={1} />
      </g>
      <g className="dg-labels" fill="currentColor" stroke="none" fontFamily="var(--font-mono)" fontSize="16">
        <text x={6 * CELL} y={7 * CELL - 8} textAnchor="middle">
          b
        </text>
        <text x={10 * CELL + 10} y={4.5 * CELL + 5}>d₁</text>
        <text x={9.7 * CELL} y={1.5 * CELL - 8}>R</text>
        <text x={0} y={3 * CELL - 8} fontSize="12" opacity="0.8">
          ±0.000
        </text>
      </g>
    </svg>
  )
}
