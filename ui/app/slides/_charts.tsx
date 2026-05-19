"use client";

import type { RubricPayload } from "./_chartData";

const JUDGE_COLORS: Record<string, string> = {
  "claude-sonnet-4-6": "#7AA2F7",
  "gpt-4o": "#E5A55B",
};

const JUDGE_SHORT: Record<string, string> = {
  "claude-sonnet-4-6": "Claude Sonnet 4.6",
  "gpt-4o": "GPT-4o",
};

function clamp(v: number, lo: number, hi: number) {
  return Math.max(lo, Math.min(hi, v));
}

/**
 * Per-item Δ chart — one bar per (item × judge).
 * Bleed items rendered with a hatched/lighter fill to call out the confound.
 */
export function PerItemDeltaChart({
  payload,
  height = 360,
  width = 720,
  maxDelta = 2.0,
}: {
  payload: RubricPayload;
  height?: number;
  width?: number;
  maxDelta?: number;
}) {
  const labelW = 240;
  const padL = labelW + 12;
  const padR = 36;
  const padT = 28;
  const padB = 28;
  const plotW = width - padL - padR;
  const plotH = height - padT - padB;

  const nItems = payload.items.length;
  const rowH = plotH / nItems;
  const barH = 9;
  const judges = payload.judges;
  const judgeGap = 2;
  const groupH = judges.length * barH + (judges.length - 1) * judgeGap;
  const groupTopOffset = (rowH - groupH) / 2;

  const scaleX = (v: number) => (clamp(v, 0, maxDelta) / maxDelta) * plotW;

  // Tick marks at 0, 0.5, 1.0, 1.5, 2.0
  const ticks = [0, 0.5, 1.0, 1.5, 2.0].filter((t) => t <= maxDelta);

  return (
    <svg
      viewBox={`0 0 ${width} ${height}`}
      role="img"
      aria-label={`Per-item delta chart, ${payload.rubric}`}
      className="w-full"
    >
      {/* Vertical grid + ticks */}
      {ticks.map((t) => {
        const x = padL + scaleX(t);
        return (
          <g key={t}>
            <line
              x1={x}
              x2={x}
              y1={padT}
              y2={padT + plotH}
              stroke="#2a2f3a"
              strokeDasharray={t === 0 ? "0" : "3 4"}
              strokeWidth={t === 0 ? 1.5 : 1}
            />
            <text
              x={x}
              y={padT + plotH + 18}
              fontSize="11"
              fill="#9aa3b3"
              textAnchor="middle"
              fontFamily="ui-monospace, SFMono-Regular, monospace"
            >
              {t.toFixed(1)}
            </text>
          </g>
        );
      })}

      {/* Items */}
      {payload.items.map((item, i) => {
        const rowTop = padT + i * rowH;
        return (
          <g key={item.n}>
            {/* Row separator */}
            {i > 0 && (
              <line
                x1={12}
                x2={width - 12}
                y1={rowTop}
                y2={rowTop}
                stroke="#1d212a"
                strokeWidth={1}
              />
            )}
            {/* Item label */}
            <text
              x={padL - 10}
              y={rowTop + rowH / 2 + 4}
              fontSize="12.5"
              fill={item.isBleed ? "#E5A55B" : "#d6dae3"}
              textAnchor="end"
              fontWeight={item.isBleed ? 600 : 400}
            >
              <tspan fontFamily="ui-monospace, SFMono-Regular, monospace" fill="#6a7180">
                {String(item.n).padStart(2, " ")}.
              </tspan>
              <tspan dx="6">{item.label}</tspan>
            </text>
            {/* Judge bars */}
            {judges.map((judge, j) => {
              const y = rowTop + groupTopOffset + j * (barH + judgeGap);
              const delta = payload.v1.deltas[judge]?.[item.n] ?? 0;
              const w = scaleX(delta);
              return (
                <g key={judge}>
                  <rect
                    x={padL}
                    y={y}
                    width={Math.max(0, w)}
                    height={barH}
                    fill={JUDGE_COLORS[judge] ?? "#6a7180"}
                    opacity={item.isBleed ? 0.95 : 0.75}
                    rx={1.5}
                  />
                  <text
                    x={padL + w + 6}
                    y={y + barH - 1}
                    fontSize="10.5"
                    fill="#9aa3b3"
                    fontFamily="ui-monospace, SFMono-Regular, monospace"
                  >
                    {delta >= 0 ? `+${delta.toFixed(2)}` : delta.toFixed(2)}
                  </text>
                </g>
              );
            })}
          </g>
        );
      })}

      {/* Legend */}
      <g transform={`translate(${padL}, 14)`}>
        {judges.map((judge, i) => (
          <g key={judge} transform={`translate(${i * 180}, 0)`}>
            <rect width={16} height={9} y={-2} fill={JUDGE_COLORS[judge]} rx={1.5} />
            <text x={22} y={7} fontSize="11.5" fill="#d6dae3">
              {JUDGE_SHORT[judge] ?? judge}
            </text>
          </g>
        ))}
      </g>
    </svg>
  );
}

/**
 * v1 vs v2 comparison — focused on bleed-detection items only.
 * Two bars per (item × judge): v1 Δ above, v2 Δ below.
 */
export function BleedV1V2Chart({
  payload,
  height = 280,
  width = 720,
  maxDelta = 2.0,
}: {
  payload: RubricPayload;
  height?: number;
  width?: number;
  maxDelta?: number;
}) {
  if (!payload.v2) return null;
  const bleedItems = payload.items.filter((it) => it.isBleed);
  if (bleedItems.length === 0) return null;

  const labelW = 240;
  const padL = labelW + 12;
  const padR = 60;
  const padT = 30;
  const padB = 28;
  const plotW = width - padL - padR;
  const plotH = height - padT - padB;
  const judges = payload.judges;

  const rowH = plotH / bleedItems.length;
  const barH = 10;
  const versionGap = 4;
  const judgeGap = 14;
  // Layout per item: for each judge, stack v1 on top, v2 below.
  const perJudgeH = barH * 2 + versionGap;
  const groupH = judges.length * perJudgeH + (judges.length - 1) * judgeGap;
  const groupTopOffset = (rowH - groupH) / 2;
  const scaleX = (v: number) => (clamp(v, 0, maxDelta) / maxDelta) * plotW;
  const ticks = [0, 0.5, 1.0, 1.5, 2.0].filter((t) => t <= maxDelta);

  return (
    <svg
      viewBox={`0 0 ${width} ${height}`}
      role="img"
      aria-label={`v1 vs v2 bleed-item delta, ${payload.rubric}`}
      className="w-full"
    >
      {ticks.map((t) => {
        const x = padL + scaleX(t);
        return (
          <g key={t}>
            <line
              x1={x}
              x2={x}
              y1={padT}
              y2={padT + plotH}
              stroke="#2a2f3a"
              strokeDasharray={t === 0 ? "0" : "3 4"}
              strokeWidth={t === 0 ? 1.5 : 1}
            />
            <text
              x={x}
              y={padT + plotH + 18}
              fontSize="11"
              fill="#9aa3b3"
              textAnchor="middle"
              fontFamily="ui-monospace, SFMono-Regular, monospace"
            >
              {t.toFixed(1)}
            </text>
          </g>
        );
      })}

      {bleedItems.map((item, i) => {
        const rowTop = padT + i * rowH;
        return (
          <g key={item.n}>
            {i > 0 && (
              <line
                x1={12}
                x2={width - 12}
                y1={rowTop}
                y2={rowTop}
                stroke="#1d212a"
                strokeWidth={1}
              />
            )}
            <text
              x={padL - 10}
              y={rowTop + rowH / 2 + 4}
              fontSize="12.5"
              fill="#E5A55B"
              textAnchor="end"
              fontWeight={600}
            >
              <tspan fontFamily="ui-monospace, SFMono-Regular, monospace" fill="#9aa3b3">
                {String(item.n).padStart(2, " ")}.
              </tspan>
              <tspan dx="6">{item.label}</tspan>
            </text>
            {judges.map((judge, j) => {
              const yBase = rowTop + groupTopOffset + j * (perJudgeH + judgeGap);
              const v1 = payload.v1.deltas[judge]?.[item.n] ?? 0;
              const v2 = payload.v2?.deltas[judge]?.[item.n] ?? 0;
              const diff = v2 - v1;
              return (
                <g key={judge}>
                  {/* v1 bar */}
                  <rect
                    x={padL}
                    y={yBase}
                    width={Math.max(0, scaleX(v1))}
                    height={barH}
                    fill={JUDGE_COLORS[judge] ?? "#6a7180"}
                    opacity={0.45}
                    rx={1.5}
                  />
                  <text
                    x={padL + scaleX(v1) + 6}
                    y={yBase + barH - 1}
                    fontSize="10"
                    fill="#9aa3b3"
                    fontFamily="ui-monospace, SFMono-Regular, monospace"
                  >
                    v1 {v1 >= 0 ? `+${v1.toFixed(2)}` : v1.toFixed(2)}
                  </text>
                  {/* v2 bar */}
                  <rect
                    x={padL}
                    y={yBase + barH + versionGap}
                    width={Math.max(0, scaleX(v2))}
                    height={barH}
                    fill={JUDGE_COLORS[judge] ?? "#6a7180"}
                    opacity={0.95}
                    rx={1.5}
                  />
                  <text
                    x={padL + scaleX(v2) + 6}
                    y={yBase + barH * 2 + versionGap - 1}
                    fontSize="10"
                    fill="#d6dae3"
                    fontFamily="ui-monospace, SFMono-Regular, monospace"
                  >
                    v2 {v2 >= 0 ? `+${v2.toFixed(2)}` : v2.toFixed(2)}
                    <tspan
                      dx="6"
                      fill={diff < -0.05 ? "#7CCF7C" : diff > 0.05 ? "#E58787" : "#6a7180"}
                    >
                      ({diff >= 0 ? `+${diff.toFixed(2)}` : diff.toFixed(2)})
                    </tspan>
                  </text>
                </g>
              );
            })}
          </g>
        );
      })}

      {/* Legend */}
      <g transform={`translate(${padL}, 14)`}>
        {judges.map((judge, i) => (
          <g key={judge} transform={`translate(${i * 200}, 0)`}>
            <rect width={12} height={8} y={-2} fill={JUDGE_COLORS[judge]} opacity={0.45} rx={1.5} />
            <rect width={12} height={8} y={9} fill={JUDGE_COLORS[judge]} opacity={0.95} rx={1.5} />
            <text x={20} y={5} fontSize="11" fill="#9aa3b3">
              v1 · {JUDGE_SHORT[judge] ?? judge}
            </text>
            <text x={20} y={17} fontSize="11" fill="#d6dae3">
              v2 · {JUDGE_SHORT[judge] ?? judge}
            </text>
          </g>
        ))}
      </g>
    </svg>
  );
}
