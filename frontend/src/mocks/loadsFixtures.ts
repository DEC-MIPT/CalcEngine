import type { components } from '../api/schema'

type CalculationTypeView = components['schemas']['CalculationTypeView']

type CalculationRequest = components['schemas']['CalculationRequest']

type ResultEnvelope = components['schemas']['ResultEnvelope']

type ParameterSourceInfo = components['schemas']['ParameterSourceInfo']

export const LOADS_TYPE = 'foundations_shallow_loads'

export const loadsCalculationType = {
  "name": "foundations_shallow_loads",
  "inputs": [
    {
      "name": "b",
      "base_unit": "m",
      "dimension": "length",
      "units": [
        "m",
        "cm",
        "mm"
      ],
      "label": {
        "ru": "Ширина подошвы фундамента",
        "en": "Foundation base width"
      },
      "symbol": "b",
      "hint": null,
      "whole_values_only": false
    },
    {
      "name": "d_1",
      "base_unit": "m",
      "dimension": "length",
      "units": [
        "m",
        "cm",
        "mm"
      ],
      "label": {
        "ru": "Приведённая глубина заложения",
        "en": "Reduced foundation depth"
      },
      "symbol": "d_1",
      "hint": {
        "ru": "Значение, вычисленное отдельно; здесь оно вводится готовым",
        "en": "A value calculated separately and entered as is"
      },
      "whole_values_only": false
    },
    {
      "name": "d_b",
      "base_unit": "m",
      "dimension": "length",
      "units": [
        "m",
        "cm",
        "mm"
      ],
      "label": {
        "ru": "Глубина подвала",
        "en": "Basement depth"
      },
      "symbol": "d_b",
      "hint": null,
      "whole_values_only": false
    },
    {
      "name": "gamma_II",
      "base_unit": "kN/m3",
      "dimension": "specific_weight",
      "units": [
        "N/m3",
        "kN/m3"
      ],
      "label": {
        "ru": "Удельный вес грунта ниже подошвы",
        "en": "Unit weight of soil below the base"
      },
      "symbol": "\\gamma_{II}",
      "hint": null,
      "whole_values_only": false
    },
    {
      "name": "gamma_II_prime",
      "base_unit": "kN/m3",
      "dimension": "specific_weight",
      "units": [
        "N/m3",
        "kN/m3"
      ],
      "label": {
        "ru": "Удельный вес грунта выше подошвы",
        "en": "Unit weight of soil above the base"
      },
      "symbol": "\\gamma'_{II}",
      "hint": null,
      "whole_values_only": false
    },
    {
      "name": "c_II",
      "base_unit": "kPa",
      "dimension": "pressure",
      "units": [
        "Pa",
        "kPa",
        "MPa"
      ],
      "label": {
        "ru": "Удельное сцепление грунта",
        "en": "Soil cohesion"
      },
      "symbol": "c_{II}",
      "hint": null,
      "whole_values_only": false
    },
    {
      "name": "phi_II",
      "base_unit": "deg",
      "dimension": "angle",
      "units": [
        "rad",
        "deg"
      ],
      "label": {
        "ru": "Угол внутреннего трения грунта",
        "en": "Soil friction angle"
      },
      "symbol": "\\varphi_{II}",
      "hint": {
        "ru": "Целое число градусов: коэффициенты выбираются по строке таблицы",
        "en": "A whole number of degrees: the coefficients are chosen by a table row"
      },
      "whole_values_only": true
    },
    {
      "name": "l",
      "base_unit": "m",
      "dimension": "length",
      "units": [
        "m",
        "cm",
        "mm"
      ],
      "label": {
        "ru": "Длина подошвы по оси y",
        "en": null
      },
      "symbol": "l",
      "hint": {
        "ru": "l ≥ b; стороны и нагрузки автоматически не переставляются",
        "en": null
      },
      "whole_values_only": false
    },
    {
      "name": "h",
      "base_unit": "m",
      "dimension": "length",
      "units": [
        "m",
        "cm",
        "mm"
      ],
      "label": {
        "ru": "Расстояние от сечения нагрузок до подошвы",
        "en": null
      },
      "symbol": "h",
      "hint": {
        "ru": "Независимо от d и d_1; моменты переносятся по M+Q*h",
        "en": null
      },
      "whole_values_only": false
    },
    {
      "name": "d",
      "base_unit": "m",
      "dimension": "length",
      "units": [
        "m",
        "cm",
        "mm"
      ],
      "label": {
        "ru": "Толщина в весовом слагаемом",
        "en": null
      },
      "symbol": "d",
      "hint": {
        "ru": "Независима от h и d_1; вес учитывается через γ_mt*d",
        "en": null
      },
      "whole_values_only": false
    },
    {
      "name": "N",
      "base_unit": "kN",
      "dimension": "force",
      "units": [
        "N",
        "kN",
        "MN"
      ],
      "label": {
        "ru": "Вертикальная нагрузка",
        "en": null
      },
      "symbol": "N",
      "hint": {
        "ru": "Без собственного веса фундамента и грунта над подошвой; вес добавляется один раз",
        "en": null
      },
      "whole_values_only": false
    },
    {
      "name": "Mx",
      "base_unit": "kN*m",
      "dimension": "moment",
      "units": [
        "N*m",
        "kN*m",
        "MN*m"
      ],
      "label": {
        "ru": "Подписанный момент для давления вдоль x=b",
        "en": null
      },
      "symbol": "M_x",
      "hint": null,
      "whole_values_only": false
    },
    {
      "name": "My",
      "base_unit": "kN*m",
      "dimension": "moment",
      "units": [
        "N*m",
        "kN*m",
        "MN*m"
      ],
      "label": {
        "ru": "Подписанный момент для давления вдоль y=l",
        "en": null
      },
      "symbol": "M_y",
      "hint": null,
      "whole_values_only": false
    },
    {
      "name": "Qx",
      "base_unit": "kN",
      "dimension": "force",
      "units": [
        "N",
        "kN",
        "MN"
      ],
      "label": {
        "ru": "Подписанная поперечная сила вдоль x=b",
        "en": null
      },
      "symbol": "Q_x",
      "hint": null,
      "whole_values_only": false
    },
    {
      "name": "Qy",
      "base_unit": "kN",
      "dimension": "force",
      "units": [
        "N",
        "kN",
        "MN"
      ],
      "label": {
        "ru": "Подписанная поперечная сила вдоль y=l",
        "en": null
      },
      "symbol": "Q_y",
      "hint": null,
      "whole_values_only": false
    }
  ],
  "outputs": [
    {
      "name": "R",
      "base_unit": "kPa",
      "label": {
        "ru": "Расчётное сопротивление грунта",
        "en": null
      },
      "symbol": "R"
    },
    {
      "name": "p",
      "base_unit": "kPa",
      "label": {
        "ru": "Среднее давление",
        "en": null
      },
      "symbol": "p"
    },
    {
      "name": "p_x_min",
      "base_unit": "kPa",
      "label": {
        "ru": "Минимальное давление по x",
        "en": null
      },
      "symbol": "p_{x,min}"
    },
    {
      "name": "p_x_max",
      "base_unit": "kPa",
      "label": {
        "ru": "Максимальное давление по x",
        "en": null
      },
      "symbol": "p_{x,max}"
    },
    {
      "name": "p_y_min",
      "base_unit": "kPa",
      "label": {
        "ru": "Минимальное давление по y",
        "en": null
      },
      "symbol": "p_{y,min}"
    },
    {
      "name": "p_y_max",
      "base_unit": "kPa",
      "label": {
        "ru": "Максимальное давление по y",
        "en": null
      },
      "symbol": "p_{y,max}"
    },
    {
      "name": "p_corner_pp",
      "base_unit": "kPa",
      "label": {
        "ru": "Угловое давление (+x,+y)",
        "en": null
      },
      "symbol": "p_{++}"
    },
    {
      "name": "p_corner_pm",
      "base_unit": "kPa",
      "label": {
        "ru": "Угловое давление (+x,-y)",
        "en": null
      },
      "symbol": "p_{+-}"
    },
    {
      "name": "p_corner_mp",
      "base_unit": "kPa",
      "label": {
        "ru": "Угловое давление (-x,+y)",
        "en": null
      },
      "symbol": "p_{-+}"
    },
    {
      "name": "p_corner_mm",
      "base_unit": "kPa",
      "label": {
        "ru": "Угловое давление (-x,-y)",
        "en": null
      },
      "symbol": "p_{--}"
    }
  ]
} satisfies CalculationTypeView

export const LOADS_CENTRAL_ID = '55555555-5555-4555-8555-555555555555'

export const loadsCentralInputs = {
  "b": {
    "value": 2,
    "unit": "m"
  },
  "d_1": {
    "value": 1,
    "unit": "m"
  },
  "d_b": {
    "value": 0,
    "unit": "m"
  },
  "gamma_II": {
    "value": 20,
    "unit": "kN/m3"
  },
  "gamma_II_prime": {
    "value": 20,
    "unit": "kN/m3"
  },
  "c_II": {
    "value": 10,
    "unit": "kPa"
  },
  "phi_II": {
    "value": 20,
    "unit": "deg"
  },
  "l": {
    "value": 3,
    "unit": "m"
  },
  "h": {
    "value": 1,
    "unit": "m"
  },
  "d": {
    "value": 1,
    "unit": "m"
  },
  "N": {
    "value": 600,
    "unit": "kN"
  },
  "Mx": {
    "value": 0,
    "unit": "kN*m"
  },
  "My": {
    "value": 0,
    "unit": "kN*m"
  },
  "Qx": {
    "value": 0,
    "unit": "kN"
  },
  "Qy": {
    "value": 0,
    "unit": "kN"
  }
} satisfies CalculationRequest['inputs']

export const loadsCentralEnvelope = {
  "engine_version": "0.1.0",
  "input_hash": "22c0d8c6334ed14ddcc4f326eda3c8c7f7fc740a1c4890f4fb269ad45be4a552", // pragma: allowlist secret
  "outputs": [
    {
      "value": 152.02,
      "unit": "kPa",
      "quantity": "R",
      "rounding_rule": {
        "decimals": 2,
        "mode": "half_up"
      },
      "rounding_source": {
        "engineer": "Аким",
        "rationale": "Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются."
      }
    },
    {
      "value": 120.0,
      "unit": "kPa",
      "quantity": "p",
      "rounding_rule": {
        "decimals": 2,
        "mode": "half_up"
      },
      "rounding_source": {
        "engineer": "Аким",
        "rationale": "Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются."
      }
    },
    {
      "value": 120.0,
      "unit": "kPa",
      "quantity": "p_x_min",
      "rounding_rule": {
        "decimals": 2,
        "mode": "half_up"
      },
      "rounding_source": {
        "engineer": "Аким",
        "rationale": "Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются."
      }
    },
    {
      "value": 120.0,
      "unit": "kPa",
      "quantity": "p_x_max",
      "rounding_rule": {
        "decimals": 2,
        "mode": "half_up"
      },
      "rounding_source": {
        "engineer": "Аким",
        "rationale": "Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются."
      }
    },
    {
      "value": 120.0,
      "unit": "kPa",
      "quantity": "p_y_min",
      "rounding_rule": {
        "decimals": 2,
        "mode": "half_up"
      },
      "rounding_source": {
        "engineer": "Аким",
        "rationale": "Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются."
      }
    },
    {
      "value": 120.0,
      "unit": "kPa",
      "quantity": "p_y_max",
      "rounding_rule": {
        "decimals": 2,
        "mode": "half_up"
      },
      "rounding_source": {
        "engineer": "Аким",
        "rationale": "Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются."
      }
    },
    {
      "value": 120.0,
      "unit": "kPa",
      "quantity": "p_corner_pp",
      "rounding_rule": {
        "decimals": 2,
        "mode": "half_up"
      },
      "rounding_source": {
        "engineer": "Аким",
        "rationale": "Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются."
      }
    },
    {
      "value": 120.0,
      "unit": "kPa",
      "quantity": "p_corner_pm",
      "rounding_rule": {
        "decimals": 2,
        "mode": "half_up"
      },
      "rounding_source": {
        "engineer": "Аким",
        "rationale": "Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются."
      }
    },
    {
      "value": 120.0,
      "unit": "kPa",
      "quantity": "p_corner_mp",
      "rounding_rule": {
        "decimals": 2,
        "mode": "half_up"
      },
      "rounding_source": {
        "engineer": "Аким",
        "rationale": "Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются."
      }
    },
    {
      "value": 120.0,
      "unit": "kPa",
      "quantity": "p_corner_mm",
      "rounding_rule": {
        "decimals": 2,
        "mode": "half_up"
      },
      "rounding_source": {
        "engineer": "Аким",
        "rationale": "Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются."
      }
    }
  ],
  "norm_refs": [
    {
      "document": "СП 22.13330.2016",
      "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
      "clause": "5.6.7, таблица 5.4",
      "status": "unverified",
      "provenance": "machine-extracted"
    },
    {
      "document": "СП 22.13330.2016",
      "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
      "clause": "5.6.7, экспликация k",
      "status": "unverified",
      "provenance": "machine-extracted"
    },
    {
      "document": "СП 22.13330.2016",
      "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
      "clause": "5.6.7, таблица 5.5",
      "status": "unverified",
      "provenance": "machine-extracted"
    },
    {
      "document": "СП 22.13330.2016",
      "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
      "clause": "5.6.7, экспликация k_z",
      "status": "unverified",
      "provenance": "machine-extracted"
    },
    {
      "document": "СП 22.13330.2016",
      "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
      "clause": "5.6.7, формула (5.7)",
      "status": "unverified",
      "provenance": "machine-extracted"
    },
    {
      "document": "СП 22.13330.2016",
      "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
      "clause": "5.6.28, explanation of formula (5.11)",
      "status": "unverified",
      "provenance": "machine-extracted"
    },
    {
      "document": "СП 22.13330.2016",
      "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
      "clause": "5.6.28, formula (5.11)",
      "status": "unverified",
      "provenance": "machine-extracted"
    },
    {
      "document": "СП 22.13330.2016",
      "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
      "clause": "5.6.28, applicability of formula (5.11)",
      "status": "unverified",
      "provenance": "machine-extracted"
    },
    {
      "document": "СП 22.13330.2016",
      "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
      "clause": "5.6.27, figure 5.1",
      "status": "unverified",
      "provenance": "machine-extracted"
    },
    {
      "document": "СП 22.13330.2016",
      "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
      "clause": "5.6.29, formula (5.15)",
      "status": "unverified",
      "provenance": "machine-extracted"
    },
    {
      "document": "СП 22.13330.2016",
      "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
      "clause": "5.6.26",
      "status": "unverified",
      "provenance": "machine-extracted"
    },
    {
      "document": "СП 22.13330.2016",
      "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
      "clause": "5.6.7",
      "status": "unverified",
      "provenance": "machine-extracted"
    }
  ],
  "engineer_rules": [
    {
      "engineer": "Аким",
      "rationale": "Геометрия прямоугольной подошвы: A=b*l, Wx=l*b²/6, Wy=b*l²/6; инженерный контракт 2026-11-08."
    },
    {
      "engineer": "Аким",
      "rationale": "Подписанный перенос нагрузок к подошве M_base=M+Q*h; оси x=b и y=l; инженерный контракт 2026-11-08."
    },
    {
      "engineer": "Аким",
      "rationale": "Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08."
    },
    {
      "engineer": "Аким",
      "rationale": "Полный контакт прямоугольной подошвы: минимум четырёх подписанных угловых давлений неотрицателен; решение инженера 2026-11-08."
    },
    {
      "engineer": "Аким",
      "rationale": "Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются."
    }
  ],
  "verdict": "pass",
  "verdict_reason": {
    "kind": "check",
    "step_id": "p_corner_max_le_limit"
  },
  "warnings": [],
  "trace": [
    {
      "step_id": "gamma_c1",
      "expression": "\\gamma_{c1}",
      "substitutions": [],
      "result": {
        "value": 1.1,
        "unit": "1"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.7, таблица 5.4",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "table"
    },
    {
      "step_id": "gamma_c2",
      "expression": "\\gamma_{c2}",
      "substitutions": [],
      "result": {
        "value": 1.0,
        "unit": "1"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.7, таблица 5.4",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "table"
    },
    {
      "step_id": "k",
      "expression": "k",
      "substitutions": [],
      "result": {
        "value": 1.0,
        "unit": "1"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.7, экспликация k",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "table"
    },
    {
      "step_id": "M_gamma",
      "expression": "M_{\\gamma} = M_{\\gamma}\\left(\\varphi_{II}\\right)",
      "substitutions": [
        {
          "value": 20.0,
          "unit": "deg",
          "symbol": "phi_II"
        }
      ],
      "result": {
        "value": 0.51,
        "unit": "1"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.7, таблица 5.5",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "table"
    },
    {
      "step_id": "M_q",
      "expression": "M_{q} = M_{q}\\left(\\varphi_{II}\\right)",
      "substitutions": [
        {
          "value": 20.0,
          "unit": "deg",
          "symbol": "phi_II"
        }
      ],
      "result": {
        "value": 3.06,
        "unit": "1"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.7, таблица 5.5",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "table"
    },
    {
      "step_id": "M_c",
      "expression": "M_{c} = M_{c}\\left(\\varphi_{II}\\right)",
      "substitutions": [
        {
          "value": 20.0,
          "unit": "deg",
          "symbol": "phi_II"
        }
      ],
      "result": {
        "value": 5.66,
        "unit": "1"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.7, таблица 5.5",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "table"
    },
    {
      "step_id": "k_z",
      "expression": "k_{z}=1",
      "substitutions": [],
      "result": {
        "value": 1.0,
        "unit": "1"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.7, экспликация k_z",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "step_id": "R",
      "expression": "R=\\frac{\\gamma_{c1}\\gamma_{c2}}{k}\\left[M_{\\gamma}k_{z}b\\gamma_{II}+M_{q}d_{1}\\gamma'_{II}+(M_{q}-1)d_{b}\\gamma'_{II}+M_{c}c_{II}\\right]",
      "substitutions": [
        {
          "value": 1.1,
          "unit": "1",
          "symbol": "gamma_c1"
        },
        {
          "value": 1.0,
          "unit": "1",
          "symbol": "gamma_c2"
        },
        {
          "value": 1.0,
          "unit": "1",
          "symbol": "k"
        },
        {
          "value": 0.51,
          "unit": "1",
          "symbol": "M_gamma"
        },
        {
          "value": 1.0,
          "unit": "1",
          "symbol": "k_z"
        },
        {
          "value": 2.0,
          "unit": "m",
          "symbol": "b"
        },
        {
          "value": 20.0,
          "unit": "kN/m3",
          "symbol": "gamma_II"
        },
        {
          "value": 3.06,
          "unit": "1",
          "symbol": "M_q"
        },
        {
          "value": 1.0,
          "unit": "m",
          "symbol": "d_1"
        },
        {
          "value": 20.0,
          "unit": "kN/m3",
          "symbol": "gamma_II_prime"
        },
        {
          "value": 0.0,
          "unit": "m",
          "symbol": "d_b"
        },
        {
          "value": 5.66,
          "unit": "1",
          "symbol": "M_c"
        },
        {
          "value": 10.0,
          "unit": "kPa",
          "symbol": "c_II"
        }
      ],
      "result": {
        "value": 152.02,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.7, формула (5.7)",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "kind": "engineer_formula",
      "step_id": "A",
      "expression": "A=b l",
      "substitutions": [
        {
          "value": 2.0,
          "unit": "m",
          "symbol": "b"
        },
        {
          "value": 3.0,
          "unit": "m",
          "symbol": "l"
        }
      ],
      "result": {
        "value": 6.0,
        "unit": "m2"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Геометрия прямоугольной подошвы: A=b*l, Wx=l*b²/6, Wy=b*l²/6; инженерный контракт 2026-11-08."
      }
    },
    {
      "kind": "engineer_formula",
      "step_id": "Wx",
      "expression": "W_x=l b^2/6",
      "substitutions": [
        {
          "value": 2.0,
          "unit": "m",
          "symbol": "b"
        },
        {
          "value": 3.0,
          "unit": "m",
          "symbol": "l"
        }
      ],
      "result": {
        "value": 2.0,
        "unit": "m3"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Геометрия прямоугольной подошвы: A=b*l, Wx=l*b²/6, Wy=b*l²/6; инженерный контракт 2026-11-08."
      }
    },
    {
      "kind": "engineer_formula",
      "step_id": "Wy",
      "expression": "W_y=b l^2/6",
      "substitutions": [
        {
          "value": 2.0,
          "unit": "m",
          "symbol": "b"
        },
        {
          "value": 3.0,
          "unit": "m",
          "symbol": "l"
        }
      ],
      "result": {
        "value": 3.0,
        "unit": "m3"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Геометрия прямоугольной подошвы: A=b*l, Wx=l*b²/6, Wy=b*l²/6; инженерный контракт 2026-11-08."
      }
    },
    {
      "kind": "engineer_formula",
      "step_id": "Mx_base",
      "expression": "M_{x,base}=M_x+Q_x h",
      "substitutions": [
        {
          "value": 0.0,
          "unit": "kN*m",
          "symbol": "Mx"
        },
        {
          "value": 0.0,
          "unit": "kN",
          "symbol": "Qx"
        },
        {
          "value": 1.0,
          "unit": "m",
          "symbol": "h"
        }
      ],
      "result": {
        "value": 0.0,
        "unit": "kN*m"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Подписанный перенос нагрузок к подошве M_base=M+Q*h; оси x=b и y=l; инженерный контракт 2026-11-08."
      }
    },
    {
      "kind": "engineer_formula",
      "step_id": "My_base",
      "expression": "M_{y,base}=M_y+Q_y h",
      "substitutions": [
        {
          "value": 0.0,
          "unit": "kN*m",
          "symbol": "My"
        },
        {
          "value": 0.0,
          "unit": "kN",
          "symbol": "Qy"
        },
        {
          "value": 1.0,
          "unit": "m",
          "symbol": "h"
        }
      ],
      "result": {
        "value": 0.0,
        "unit": "kN*m"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Подписанный перенос нагрузок к подошве M_base=M+Q*h; оси x=b и y=l; инженерный контракт 2026-11-08."
      }
    },
    {
      "step_id": "gamma_mt",
      "expression": "\\gamma_{mt}",
      "substitutions": [],
      "result": {
        "value": 20.0,
        "unit": "kN/m3"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.28, explanation of formula (5.11)",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "table"
    },
    {
      "step_id": "p",
      "expression": "p_{+}=\\frac{N}{A}+\\gamma_{mt}d+\\frac{M}{W}",
      "substitutions": [
        {
          "value": 600.0,
          "unit": "kN",
          "symbol": "N"
        },
        {
          "value": 6.0,
          "unit": "m2",
          "symbol": "A"
        },
        {
          "value": 20.0,
          "unit": "kN/m3",
          "symbol": "gamma_mt"
        },
        {
          "value": 1.0,
          "unit": "m",
          "symbol": "d"
        },
        {
          "value": 0.0,
          "unit": "kN*m",
          "symbol": "M"
        },
        {
          "value": 2.0,
          "unit": "m3",
          "symbol": "W"
        }
      ],
      "result": {
        "value": 120.0,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.28, formula (5.11)",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "kind": "engineer_formula",
      "step_id": "V",
      "expression": "V=N+\\gamma_{mt} d A",
      "substitutions": [
        {
          "value": 600.0,
          "unit": "kN",
          "symbol": "N"
        },
        {
          "value": 20.0,
          "unit": "kN/m3",
          "symbol": "gamma_mt"
        },
        {
          "value": 1.0,
          "unit": "m",
          "symbol": "d"
        },
        {
          "value": 6.0,
          "unit": "m2",
          "symbol": "A"
        }
      ],
      "result": {
        "value": 720.0,
        "unit": "kN"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08."
      }
    },
    {
      "step_id": "p_x_min",
      "expression": "p_{-}=\\frac{N}{A}+\\gamma_{mt}d-\\frac{M}{W}",
      "substitutions": [
        {
          "value": 600.0,
          "unit": "kN",
          "symbol": "N"
        },
        {
          "value": 6.0,
          "unit": "m2",
          "symbol": "A"
        },
        {
          "value": 20.0,
          "unit": "kN/m3",
          "symbol": "gamma_mt"
        },
        {
          "value": 1.0,
          "unit": "m",
          "symbol": "d"
        },
        {
          "value": 0.0,
          "unit": "kN*m",
          "symbol": "M"
        },
        {
          "value": 2.0,
          "unit": "m3",
          "symbol": "W"
        }
      ],
      "result": {
        "value": 120.0,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.28, formula (5.11)",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "step_id": "p_x_max",
      "expression": "p_{+}=\\frac{N}{A}+\\gamma_{mt}d+\\frac{M}{W}",
      "substitutions": [
        {
          "value": 600.0,
          "unit": "kN",
          "symbol": "N"
        },
        {
          "value": 6.0,
          "unit": "m2",
          "symbol": "A"
        },
        {
          "value": 20.0,
          "unit": "kN/m3",
          "symbol": "gamma_mt"
        },
        {
          "value": 1.0,
          "unit": "m",
          "symbol": "d"
        },
        {
          "value": 0.0,
          "unit": "kN*m",
          "symbol": "M"
        },
        {
          "value": 2.0,
          "unit": "m3",
          "symbol": "W"
        }
      ],
      "result": {
        "value": 120.0,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.28, formula (5.11)",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "kind": "engineer_formula",
      "step_id": "e_x",
      "expression": "e_x=|M_{x,base}|/V",
      "substitutions": [
        {
          "value": 0.0,
          "unit": "kN*m",
          "symbol": "Mx_base"
        },
        {
          "value": 720.0,
          "unit": "kN",
          "symbol": "V"
        }
      ],
      "result": {
        "value": 0.0,
        "unit": "m"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08."
      }
    },
    {
      "step_id": "relative_eccentricity_x",
      "expression": "e/l\\leq1/6",
      "substitutions": [
        {
          "value": 0.0,
          "unit": "1",
          "symbol": "e/L"
        },
        {
          "value": 1.0,
          "unit": "1",
          "symbol": "numerator"
        },
        {
          "value": 6.0,
          "unit": "1",
          "symbol": "denominator"
        }
      ],
      "result": {
        "value": 1.0,
        "unit": "1"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.28, applicability of formula (5.11)",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "step_id": "pressure_diagram_x",
      "expression": "e<l/6",
      "substitutions": [
        {
          "value": 0.0,
          "unit": "m",
          "symbol": "e"
        },
        {
          "value": 2.0,
          "unit": "m",
          "symbol": "l"
        }
      ],
      "result": {
        "value": 0.0,
        "unit": "m"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.27, figure 5.1",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "step_id": "p_y_min",
      "expression": "p_{-}=\\frac{N}{A}+\\gamma_{mt}d-\\frac{M}{W}",
      "substitutions": [
        {
          "value": 600.0,
          "unit": "kN",
          "symbol": "N"
        },
        {
          "value": 6.0,
          "unit": "m2",
          "symbol": "A"
        },
        {
          "value": 20.0,
          "unit": "kN/m3",
          "symbol": "gamma_mt"
        },
        {
          "value": 1.0,
          "unit": "m",
          "symbol": "d"
        },
        {
          "value": 0.0,
          "unit": "kN*m",
          "symbol": "M"
        },
        {
          "value": 3.0,
          "unit": "m3",
          "symbol": "W"
        }
      ],
      "result": {
        "value": 120.0,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.28, formula (5.11)",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "step_id": "p_y_max",
      "expression": "p_{+}=\\frac{N}{A}+\\gamma_{mt}d+\\frac{M}{W}",
      "substitutions": [
        {
          "value": 600.0,
          "unit": "kN",
          "symbol": "N"
        },
        {
          "value": 6.0,
          "unit": "m2",
          "symbol": "A"
        },
        {
          "value": 20.0,
          "unit": "kN/m3",
          "symbol": "gamma_mt"
        },
        {
          "value": 1.0,
          "unit": "m",
          "symbol": "d"
        },
        {
          "value": 0.0,
          "unit": "kN*m",
          "symbol": "M"
        },
        {
          "value": 3.0,
          "unit": "m3",
          "symbol": "W"
        }
      ],
      "result": {
        "value": 120.0,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.28, formula (5.11)",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "kind": "engineer_formula",
      "step_id": "e_y",
      "expression": "e_y=|M_{y,base}|/V",
      "substitutions": [
        {
          "value": 0.0,
          "unit": "kN*m",
          "symbol": "My_base"
        },
        {
          "value": 720.0,
          "unit": "kN",
          "symbol": "V"
        }
      ],
      "result": {
        "value": 0.0,
        "unit": "m"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08."
      }
    },
    {
      "step_id": "relative_eccentricity_y",
      "expression": "e/l\\leq1/6",
      "substitutions": [
        {
          "value": 0.0,
          "unit": "1",
          "symbol": "e/L"
        },
        {
          "value": 1.0,
          "unit": "1",
          "symbol": "numerator"
        },
        {
          "value": 6.0,
          "unit": "1",
          "symbol": "denominator"
        }
      ],
      "result": {
        "value": 1.0,
        "unit": "1"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.28, applicability of formula (5.11)",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "step_id": "pressure_diagram_y",
      "expression": "e<l/6",
      "substitutions": [
        {
          "value": 0.0,
          "unit": "m",
          "symbol": "e"
        },
        {
          "value": 3.0,
          "unit": "m",
          "symbol": "l"
        }
      ],
      "result": {
        "value": 0.0,
        "unit": "m"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.27, figure 5.1",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "step_id": "corner_component_pp",
      "expression": "P_{\\max}=\\frac{N}{A}+\\gamma_{mt}d+\\frac{M_x}{W_x}+\\frac{M_y}{W_y}",
      "substitutions": [
        {
          "value": 600.0,
          "unit": "kN",
          "symbol": "N"
        },
        {
          "value": 6.0,
          "unit": "m2",
          "symbol": "A"
        },
        {
          "value": 20.0,
          "unit": "kN/m3",
          "symbol": "gamma_mt"
        },
        {
          "value": 1.0,
          "unit": "m",
          "symbol": "d"
        },
        {
          "value": 0.0,
          "unit": "kN*m",
          "symbol": "M_x"
        },
        {
          "value": 2.0,
          "unit": "m3",
          "symbol": "W_x"
        },
        {
          "value": 0.0,
          "unit": "kN*m",
          "symbol": "M_y"
        },
        {
          "value": 3.0,
          "unit": "m3",
          "symbol": "W_y"
        }
      ],
      "result": {
        "value": 120.0,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.29, formula (5.15)",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "kind": "engineer_formula",
      "step_id": "p_corner_pp",
      "expression": "p_{pp}=p+s_x M_{x,base}/W_x+s_y M_{y,base}/W_y",
      "substitutions": [
        {
          "value": 120.0,
          "unit": "kPa",
          "symbol": "p"
        },
        {
          "value": 0.0,
          "unit": "kN*m",
          "symbol": "Mx_base"
        },
        {
          "value": 2.0,
          "unit": "m3",
          "symbol": "Wx"
        },
        {
          "value": 0.0,
          "unit": "kN*m",
          "symbol": "My_base"
        },
        {
          "value": 3.0,
          "unit": "m3",
          "symbol": "Wy"
        },
        {
          "value": 1.0,
          "unit": "1",
          "symbol": "sign_x_pp"
        },
        {
          "value": 1.0,
          "unit": "1",
          "symbol": "sign_y_pp"
        },
        {
          "value": 120.0,
          "unit": "kPa",
          "symbol": "corner_component_pp"
        }
      ],
      "result": {
        "value": 120.0,
        "unit": "kPa"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08."
      }
    },
    {
      "step_id": "corner_component_pm",
      "expression": "P_{\\max}=\\frac{N}{A}+\\gamma_{mt}d+\\frac{M_x}{W_x}+\\frac{M_y}{W_y}",
      "substitutions": [
        {
          "value": 600.0,
          "unit": "kN",
          "symbol": "N"
        },
        {
          "value": 6.0,
          "unit": "m2",
          "symbol": "A"
        },
        {
          "value": 20.0,
          "unit": "kN/m3",
          "symbol": "gamma_mt"
        },
        {
          "value": 1.0,
          "unit": "m",
          "symbol": "d"
        },
        {
          "value": 0.0,
          "unit": "kN*m",
          "symbol": "M_x"
        },
        {
          "value": 2.0,
          "unit": "m3",
          "symbol": "W_x"
        },
        {
          "value": -0.0,
          "unit": "kN*m",
          "symbol": "M_y"
        },
        {
          "value": 3.0,
          "unit": "m3",
          "symbol": "W_y"
        }
      ],
      "result": {
        "value": 120.0,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.29, formula (5.15)",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "kind": "engineer_formula",
      "step_id": "p_corner_pm",
      "expression": "p_{pm}=p+s_x M_{x,base}/W_x+s_y M_{y,base}/W_y",
      "substitutions": [
        {
          "value": 120.0,
          "unit": "kPa",
          "symbol": "p"
        },
        {
          "value": 0.0,
          "unit": "kN*m",
          "symbol": "Mx_base"
        },
        {
          "value": 2.0,
          "unit": "m3",
          "symbol": "Wx"
        },
        {
          "value": 0.0,
          "unit": "kN*m",
          "symbol": "My_base"
        },
        {
          "value": 3.0,
          "unit": "m3",
          "symbol": "Wy"
        },
        {
          "value": 1.0,
          "unit": "1",
          "symbol": "sign_x_pm"
        },
        {
          "value": -1.0,
          "unit": "1",
          "symbol": "sign_y_pm"
        },
        {
          "value": 120.0,
          "unit": "kPa",
          "symbol": "corner_component_pm"
        }
      ],
      "result": {
        "value": 120.0,
        "unit": "kPa"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08."
      }
    },
    {
      "step_id": "corner_component_mp",
      "expression": "P_{\\max}=\\frac{N}{A}+\\gamma_{mt}d+\\frac{M_x}{W_x}+\\frac{M_y}{W_y}",
      "substitutions": [
        {
          "value": 600.0,
          "unit": "kN",
          "symbol": "N"
        },
        {
          "value": 6.0,
          "unit": "m2",
          "symbol": "A"
        },
        {
          "value": 20.0,
          "unit": "kN/m3",
          "symbol": "gamma_mt"
        },
        {
          "value": 1.0,
          "unit": "m",
          "symbol": "d"
        },
        {
          "value": -0.0,
          "unit": "kN*m",
          "symbol": "M_x"
        },
        {
          "value": 2.0,
          "unit": "m3",
          "symbol": "W_x"
        },
        {
          "value": 0.0,
          "unit": "kN*m",
          "symbol": "M_y"
        },
        {
          "value": 3.0,
          "unit": "m3",
          "symbol": "W_y"
        }
      ],
      "result": {
        "value": 120.0,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.29, formula (5.15)",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "kind": "engineer_formula",
      "step_id": "p_corner_mp",
      "expression": "p_{mp}=p+s_x M_{x,base}/W_x+s_y M_{y,base}/W_y",
      "substitutions": [
        {
          "value": 120.0,
          "unit": "kPa",
          "symbol": "p"
        },
        {
          "value": 0.0,
          "unit": "kN*m",
          "symbol": "Mx_base"
        },
        {
          "value": 2.0,
          "unit": "m3",
          "symbol": "Wx"
        },
        {
          "value": 0.0,
          "unit": "kN*m",
          "symbol": "My_base"
        },
        {
          "value": 3.0,
          "unit": "m3",
          "symbol": "Wy"
        },
        {
          "value": -1.0,
          "unit": "1",
          "symbol": "sign_x_mp"
        },
        {
          "value": 1.0,
          "unit": "1",
          "symbol": "sign_y_mp"
        },
        {
          "value": 120.0,
          "unit": "kPa",
          "symbol": "corner_component_mp"
        }
      ],
      "result": {
        "value": 120.0,
        "unit": "kPa"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08."
      }
    },
    {
      "step_id": "corner_component_mm",
      "expression": "P_{\\max}=\\frac{N}{A}+\\gamma_{mt}d+\\frac{M_x}{W_x}+\\frac{M_y}{W_y}",
      "substitutions": [
        {
          "value": 600.0,
          "unit": "kN",
          "symbol": "N"
        },
        {
          "value": 6.0,
          "unit": "m2",
          "symbol": "A"
        },
        {
          "value": 20.0,
          "unit": "kN/m3",
          "symbol": "gamma_mt"
        },
        {
          "value": 1.0,
          "unit": "m",
          "symbol": "d"
        },
        {
          "value": -0.0,
          "unit": "kN*m",
          "symbol": "M_x"
        },
        {
          "value": 2.0,
          "unit": "m3",
          "symbol": "W_x"
        },
        {
          "value": -0.0,
          "unit": "kN*m",
          "symbol": "M_y"
        },
        {
          "value": 3.0,
          "unit": "m3",
          "symbol": "W_y"
        }
      ],
      "result": {
        "value": 120.0,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.29, formula (5.15)",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "kind": "engineer_formula",
      "step_id": "p_corner_mm",
      "expression": "p_{mm}=p+s_x M_{x,base}/W_x+s_y M_{y,base}/W_y",
      "substitutions": [
        {
          "value": 120.0,
          "unit": "kPa",
          "symbol": "p"
        },
        {
          "value": 0.0,
          "unit": "kN*m",
          "symbol": "Mx_base"
        },
        {
          "value": 2.0,
          "unit": "m3",
          "symbol": "Wx"
        },
        {
          "value": 0.0,
          "unit": "kN*m",
          "symbol": "My_base"
        },
        {
          "value": 3.0,
          "unit": "m3",
          "symbol": "Wy"
        },
        {
          "value": -1.0,
          "unit": "1",
          "symbol": "sign_x_mm"
        },
        {
          "value": -1.0,
          "unit": "1",
          "symbol": "sign_y_mm"
        },
        {
          "value": 120.0,
          "unit": "kPa",
          "symbol": "corner_component_mm"
        }
      ],
      "result": {
        "value": 120.0,
        "unit": "kPa"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08."
      }
    },
    {
      "kind": "engineer_formula",
      "step_id": "p_corner_min",
      "expression": "p_{corner,min}=\\min(p_{++},p_{+-},p_{-+},p_{--})",
      "substitutions": [
        {
          "value": 120.0,
          "unit": "kPa",
          "symbol": "p_corner_pp"
        },
        {
          "value": 120.0,
          "unit": "kPa",
          "symbol": "p_corner_pm"
        },
        {
          "value": 120.0,
          "unit": "kPa",
          "symbol": "p_corner_mp"
        },
        {
          "value": 120.0,
          "unit": "kPa",
          "symbol": "p_corner_mm"
        }
      ],
      "result": {
        "value": 120.0,
        "unit": "kPa"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Полный контакт прямоугольной подошвы: минимум четырёх подписанных угловых давлений неотрицателен; решение инженера 2026-11-08."
      }
    },
    {
      "kind": "engineer_formula",
      "step_id": "p_corner_max",
      "expression": "p_{corner,max}=\\max(p_{++},p_{+-},p_{-+},p_{--})",
      "substitutions": [
        {
          "value": 120.0,
          "unit": "kPa",
          "symbol": "p_corner_pp"
        },
        {
          "value": 120.0,
          "unit": "kPa",
          "symbol": "p_corner_pm"
        },
        {
          "value": 120.0,
          "unit": "kPa",
          "symbol": "p_corner_mp"
        },
        {
          "value": 120.0,
          "unit": "kPa",
          "symbol": "p_corner_mm"
        }
      ],
      "result": {
        "value": 120.0,
        "unit": "kPa"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08."
      }
    },
    {
      "step_id": "edge_limit_multiplier",
      "expression": "edge_limit_multiplier",
      "substitutions": [],
      "result": {
        "value": 1.2,
        "unit": "1"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.26",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "table"
    },
    {
      "step_id": "edge_limit",
      "expression": "p_{edge,lim}=\\lambda_e R",
      "substitutions": [
        {
          "value": 1.2,
          "unit": "1",
          "symbol": "edge_limit_multiplier"
        },
        {
          "value": 152.02,
          "unit": "kPa",
          "symbol": "R"
        }
      ],
      "result": {
        "value": 182.424,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.26",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "step_id": "corner_limit_multiplier",
      "expression": "corner_limit_multiplier",
      "substitutions": [],
      "result": {
        "value": 1.5,
        "unit": "1"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.26",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "table"
    },
    {
      "step_id": "corner_limit",
      "expression": "p_{corner,lim}=\\lambda_c R",
      "substitutions": [
        {
          "value": 1.5,
          "unit": "1",
          "symbol": "corner_limit_multiplier"
        },
        {
          "value": 152.02,
          "unit": "kPa",
          "symbol": "R"
        }
      ],
      "result": {
        "value": 228.03000000000003,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.26",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "step_id": "p_le_R",
      "expression": "p \\le R",
      "substitutions": [
        {
          "value": 120.0,
          "unit": "kPa",
          "symbol": "p"
        },
        {
          "value": 152.02,
          "unit": "kPa",
          "symbol": "R"
        }
      ],
      "result": {
        "value": 120.0,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.7",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "check",
      "operator": "le",
      "right": {
        "value": 152.02,
        "unit": "kPa"
      },
      "passed": true
    },
    {
      "step_id": "p_x_max_le_limit",
      "expression": "p_x_max \\le edge_limit",
      "substitutions": [
        {
          "value": 120.0,
          "unit": "kPa",
          "symbol": "p_x_max"
        },
        {
          "value": 182.424,
          "unit": "kPa",
          "symbol": "edge_limit"
        }
      ],
      "result": {
        "value": 120.0,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.26",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "check",
      "operator": "le",
      "right": {
        "value": 182.424,
        "unit": "kPa"
      },
      "passed": true
    },
    {
      "step_id": "p_y_max_le_limit",
      "expression": "p_y_max \\le edge_limit",
      "substitutions": [
        {
          "value": 120.0,
          "unit": "kPa",
          "symbol": "p_y_max"
        },
        {
          "value": 182.424,
          "unit": "kPa",
          "symbol": "edge_limit"
        }
      ],
      "result": {
        "value": 120.0,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.26",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "check",
      "operator": "le",
      "right": {
        "value": 182.424,
        "unit": "kPa"
      },
      "passed": true
    },
    {
      "step_id": "p_corner_max_le_limit",
      "expression": "p_corner_max \\le corner_limit",
      "substitutions": [
        {
          "value": 120.0,
          "unit": "kPa",
          "symbol": "p_corner_max"
        },
        {
          "value": 228.03000000000003,
          "unit": "kPa",
          "symbol": "corner_limit"
        }
      ],
      "result": {
        "value": 120.0,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.26",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "check",
      "operator": "le",
      "right": {
        "value": 228.03000000000003,
        "unit": "kPa"
      },
      "passed": true
    }
  ],
  "unverified_step_count": 30,
  "result_id": "55555555-5555-4555-8555-555555555555",
  "parameter_source": {
    "kind": "interim",
    "data_sha256": "faaa0724af57ca6c8066f558c4e75c2785d099b34cbfb07c4a85892fdc3b68fe", // pragma: allowlist secret
    "profile": "strict"
  }
} satisfies ResultEnvelope

export const loadsCentralJson = "{\"engine_version\":\"0.1.0\",\"input_hash\":\"22c0d8c6334ed14ddcc4f326eda3c8c7f7fc740a1c4890f4fb269ad45be4a552\",\"outputs\":[{\"value\":152.02,\"unit\":\"kPa\",\"quantity\":\"R\",\"rounding_rule\":{\"decimals\":2,\"mode\":\"half_up\"},\"rounding_source\":{\"engineer\":\"Аким\",\"rationale\":\"Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются.\"}},{\"value\":120.0,\"unit\":\"kPa\",\"quantity\":\"p\",\"rounding_rule\":{\"decimals\":2,\"mode\":\"half_up\"},\"rounding_source\":{\"engineer\":\"Аким\",\"rationale\":\"Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются.\"}},{\"value\":120.0,\"unit\":\"kPa\",\"quantity\":\"p_x_min\",\"rounding_rule\":{\"decimals\":2,\"mode\":\"half_up\"},\"rounding_source\":{\"engineer\":\"Аким\",\"rationale\":\"Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются.\"}},{\"value\":120.0,\"unit\":\"kPa\",\"quantity\":\"p_x_max\",\"rounding_rule\":{\"decimals\":2,\"mode\":\"half_up\"},\"rounding_source\":{\"engineer\":\"Аким\",\"rationale\":\"Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются.\"}},{\"value\":120.0,\"unit\":\"kPa\",\"quantity\":\"p_y_min\",\"rounding_rule\":{\"decimals\":2,\"mode\":\"half_up\"},\"rounding_source\":{\"engineer\":\"Аким\",\"rationale\":\"Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются.\"}},{\"value\":120.0,\"unit\":\"kPa\",\"quantity\":\"p_y_max\",\"rounding_rule\":{\"decimals\":2,\"mode\":\"half_up\"},\"rounding_source\":{\"engineer\":\"Аким\",\"rationale\":\"Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются.\"}},{\"value\":120.0,\"unit\":\"kPa\",\"quantity\":\"p_corner_pp\",\"rounding_rule\":{\"decimals\":2,\"mode\":\"half_up\"},\"rounding_source\":{\"engineer\":\"Аким\",\"rationale\":\"Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются.\"}},{\"value\":120.0,\"unit\":\"kPa\",\"quantity\":\"p_corner_pm\",\"rounding_rule\":{\"decimals\":2,\"mode\":\"half_up\"},\"rounding_source\":{\"engineer\":\"Аким\",\"rationale\":\"Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются.\"}},{\"value\":120.0,\"unit\":\"kPa\",\"quantity\":\"p_corner_mp\",\"rounding_rule\":{\"decimals\":2,\"mode\":\"half_up\"},\"rounding_source\":{\"engineer\":\"Аким\",\"rationale\":\"Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются.\"}},{\"value\":120.0,\"unit\":\"kPa\",\"quantity\":\"p_corner_mm\",\"rounding_rule\":{\"decimals\":2,\"mode\":\"half_up\"},\"rounding_source\":{\"engineer\":\"Аким\",\"rationale\":\"Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются.\"}}],\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7, таблица 5.4\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"},{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7, экспликация k\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"},{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7, таблица 5.5\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"},{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7, экспликация k_z\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"},{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7, формула (5.7)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"},{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.28, explanation of formula (5.11)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"},{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.28, formula (5.11)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"},{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.28, applicability of formula (5.11)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"},{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.27, figure 5.1\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"},{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.29, formula (5.15)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"},{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.26\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"},{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"engineer_rules\":[{\"engineer\":\"Аким\",\"rationale\":\"Геометрия прямоугольной подошвы: A=b*l, Wx=l*b²/6, Wy=b*l²/6; инженерный контракт 2026-11-08.\"},{\"engineer\":\"Аким\",\"rationale\":\"Подписанный перенос нагрузок к подошве M_base=M+Q*h; оси x=b и y=l; инженерный контракт 2026-11-08.\"},{\"engineer\":\"Аким\",\"rationale\":\"Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08.\"},{\"engineer\":\"Аким\",\"rationale\":\"Полный контакт прямоугольной подошвы: минимум четырёх подписанных угловых давлений неотрицателен; решение инженера 2026-11-08.\"},{\"engineer\":\"Аким\",\"rationale\":\"Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются.\"}],\"verdict\":\"pass\",\"verdict_reason\":{\"kind\":\"check\",\"step_id\":\"p_corner_max_le_limit\"},\"warnings\":[],\"trace\":[{\"step_id\":\"gamma_c1\",\"expression\":\"\\\\gamma_{c1}\",\"substitutions\":[],\"result\":{\"value\":1.1,\"unit\":\"1\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7, таблица 5.4\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"table\"},{\"step_id\":\"gamma_c2\",\"expression\":\"\\\\gamma_{c2}\",\"substitutions\":[],\"result\":{\"value\":1.0,\"unit\":\"1\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7, таблица 5.4\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"table\"},{\"step_id\":\"k\",\"expression\":\"k\",\"substitutions\":[],\"result\":{\"value\":1.0,\"unit\":\"1\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7, экспликация k\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"table\"},{\"step_id\":\"M_gamma\",\"expression\":\"M_{\\\\gamma} = M_{\\\\gamma}\\\\left(\\\\varphi_{II}\\\\right)\",\"substitutions\":[{\"value\":20.0,\"unit\":\"deg\",\"symbol\":\"phi_II\"}],\"result\":{\"value\":0.51,\"unit\":\"1\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7, таблица 5.5\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"table\"},{\"step_id\":\"M_q\",\"expression\":\"M_{q} = M_{q}\\\\left(\\\\varphi_{II}\\\\right)\",\"substitutions\":[{\"value\":20.0,\"unit\":\"deg\",\"symbol\":\"phi_II\"}],\"result\":{\"value\":3.06,\"unit\":\"1\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7, таблица 5.5\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"table\"},{\"step_id\":\"M_c\",\"expression\":\"M_{c} = M_{c}\\\\left(\\\\varphi_{II}\\\\right)\",\"substitutions\":[{\"value\":20.0,\"unit\":\"deg\",\"symbol\":\"phi_II\"}],\"result\":{\"value\":5.66,\"unit\":\"1\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7, таблица 5.5\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"table\"},{\"step_id\":\"k_z\",\"expression\":\"k_{z}=1\",\"substitutions\":[],\"result\":{\"value\":1.0,\"unit\":\"1\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7, экспликация k_z\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"step_id\":\"R\",\"expression\":\"R=\\\\frac{\\\\gamma_{c1}\\\\gamma_{c2}}{k}\\\\left[M_{\\\\gamma}k_{z}b\\\\gamma_{II}+M_{q}d_{1}\\\\gamma'_{II}+(M_{q}-1)d_{b}\\\\gamma'_{II}+M_{c}c_{II}\\\\right]\",\"substitutions\":[{\"value\":1.1,\"unit\":\"1\",\"symbol\":\"gamma_c1\"},{\"value\":1.0,\"unit\":\"1\",\"symbol\":\"gamma_c2\"},{\"value\":1.0,\"unit\":\"1\",\"symbol\":\"k\"},{\"value\":0.51,\"unit\":\"1\",\"symbol\":\"M_gamma\"},{\"value\":1.0,\"unit\":\"1\",\"symbol\":\"k_z\"},{\"value\":2.0,\"unit\":\"m\",\"symbol\":\"b\"},{\"value\":20.0,\"unit\":\"kN/m3\",\"symbol\":\"gamma_II\"},{\"value\":3.06,\"unit\":\"1\",\"symbol\":\"M_q\"},{\"value\":1.0,\"unit\":\"m\",\"symbol\":\"d_1\"},{\"value\":20.0,\"unit\":\"kN/m3\",\"symbol\":\"gamma_II_prime\"},{\"value\":0.0,\"unit\":\"m\",\"symbol\":\"d_b\"},{\"value\":5.66,\"unit\":\"1\",\"symbol\":\"M_c\"},{\"value\":10.0,\"unit\":\"kPa\",\"symbol\":\"c_II\"}],\"result\":{\"value\":152.02,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7, формула (5.7)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"kind\":\"engineer_formula\",\"step_id\":\"A\",\"expression\":\"A=b l\",\"substitutions\":[{\"value\":2.0,\"unit\":\"m\",\"symbol\":\"b\"},{\"value\":3.0,\"unit\":\"m\",\"symbol\":\"l\"}],\"result\":{\"value\":6.0,\"unit\":\"m2\"},\"source\":{\"engineer\":\"Аким\",\"rationale\":\"Геометрия прямоугольной подошвы: A=b*l, Wx=l*b²/6, Wy=b*l²/6; инженерный контракт 2026-11-08.\"}},{\"kind\":\"engineer_formula\",\"step_id\":\"Wx\",\"expression\":\"W_x=l b^2/6\",\"substitutions\":[{\"value\":2.0,\"unit\":\"m\",\"symbol\":\"b\"},{\"value\":3.0,\"unit\":\"m\",\"symbol\":\"l\"}],\"result\":{\"value\":2.0,\"unit\":\"m3\"},\"source\":{\"engineer\":\"Аким\",\"rationale\":\"Геометрия прямоугольной подошвы: A=b*l, Wx=l*b²/6, Wy=b*l²/6; инженерный контракт 2026-11-08.\"}},{\"kind\":\"engineer_formula\",\"step_id\":\"Wy\",\"expression\":\"W_y=b l^2/6\",\"substitutions\":[{\"value\":2.0,\"unit\":\"m\",\"symbol\":\"b\"},{\"value\":3.0,\"unit\":\"m\",\"symbol\":\"l\"}],\"result\":{\"value\":3.0,\"unit\":\"m3\"},\"source\":{\"engineer\":\"Аким\",\"rationale\":\"Геометрия прямоугольной подошвы: A=b*l, Wx=l*b²/6, Wy=b*l²/6; инженерный контракт 2026-11-08.\"}},{\"kind\":\"engineer_formula\",\"step_id\":\"Mx_base\",\"expression\":\"M_{x,base}=M_x+Q_x h\",\"substitutions\":[{\"value\":0.0,\"unit\":\"kN*m\",\"symbol\":\"Mx\"},{\"value\":0.0,\"unit\":\"kN\",\"symbol\":\"Qx\"},{\"value\":1.0,\"unit\":\"m\",\"symbol\":\"h\"}],\"result\":{\"value\":0.0,\"unit\":\"kN*m\"},\"source\":{\"engineer\":\"Аким\",\"rationale\":\"Подписанный перенос нагрузок к подошве M_base=M+Q*h; оси x=b и y=l; инженерный контракт 2026-11-08.\"}},{\"kind\":\"engineer_formula\",\"step_id\":\"My_base\",\"expression\":\"M_{y,base}=M_y+Q_y h\",\"substitutions\":[{\"value\":0.0,\"unit\":\"kN*m\",\"symbol\":\"My\"},{\"value\":0.0,\"unit\":\"kN\",\"symbol\":\"Qy\"},{\"value\":1.0,\"unit\":\"m\",\"symbol\":\"h\"}],\"result\":{\"value\":0.0,\"unit\":\"kN*m\"},\"source\":{\"engineer\":\"Аким\",\"rationale\":\"Подписанный перенос нагрузок к подошве M_base=M+Q*h; оси x=b и y=l; инженерный контракт 2026-11-08.\"}},{\"step_id\":\"gamma_mt\",\"expression\":\"\\\\gamma_{mt}\",\"substitutions\":[],\"result\":{\"value\":20.0,\"unit\":\"kN/m3\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.28, explanation of formula (5.11)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"table\"},{\"step_id\":\"p\",\"expression\":\"p_{+}=\\\\frac{N}{A}+\\\\gamma_{mt}d+\\\\frac{M}{W}\",\"substitutions\":[{\"value\":600.0,\"unit\":\"kN\",\"symbol\":\"N\"},{\"value\":6.0,\"unit\":\"m2\",\"symbol\":\"A\"},{\"value\":20.0,\"unit\":\"kN/m3\",\"symbol\":\"gamma_mt\"},{\"value\":1.0,\"unit\":\"m\",\"symbol\":\"d\"},{\"value\":0.0,\"unit\":\"kN*m\",\"symbol\":\"M\"},{\"value\":2.0,\"unit\":\"m3\",\"symbol\":\"W\"}],\"result\":{\"value\":120.0,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.28, formula (5.11)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"kind\":\"engineer_formula\",\"step_id\":\"V\",\"expression\":\"V=N+\\\\gamma_{mt} d A\",\"substitutions\":[{\"value\":600.0,\"unit\":\"kN\",\"symbol\":\"N\"},{\"value\":20.0,\"unit\":\"kN/m3\",\"symbol\":\"gamma_mt\"},{\"value\":1.0,\"unit\":\"m\",\"symbol\":\"d\"},{\"value\":6.0,\"unit\":\"m2\",\"symbol\":\"A\"}],\"result\":{\"value\":720.0,\"unit\":\"kN\"},\"source\":{\"engineer\":\"Аким\",\"rationale\":\"Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08.\"}},{\"step_id\":\"p_x_min\",\"expression\":\"p_{-}=\\\\frac{N}{A}+\\\\gamma_{mt}d-\\\\frac{M}{W}\",\"substitutions\":[{\"value\":600.0,\"unit\":\"kN\",\"symbol\":\"N\"},{\"value\":6.0,\"unit\":\"m2\",\"symbol\":\"A\"},{\"value\":20.0,\"unit\":\"kN/m3\",\"symbol\":\"gamma_mt\"},{\"value\":1.0,\"unit\":\"m\",\"symbol\":\"d\"},{\"value\":0.0,\"unit\":\"kN*m\",\"symbol\":\"M\"},{\"value\":2.0,\"unit\":\"m3\",\"symbol\":\"W\"}],\"result\":{\"value\":120.0,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.28, formula (5.11)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"step_id\":\"p_x_max\",\"expression\":\"p_{+}=\\\\frac{N}{A}+\\\\gamma_{mt}d+\\\\frac{M}{W}\",\"substitutions\":[{\"value\":600.0,\"unit\":\"kN\",\"symbol\":\"N\"},{\"value\":6.0,\"unit\":\"m2\",\"symbol\":\"A\"},{\"value\":20.0,\"unit\":\"kN/m3\",\"symbol\":\"gamma_mt\"},{\"value\":1.0,\"unit\":\"m\",\"symbol\":\"d\"},{\"value\":0.0,\"unit\":\"kN*m\",\"symbol\":\"M\"},{\"value\":2.0,\"unit\":\"m3\",\"symbol\":\"W\"}],\"result\":{\"value\":120.0,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.28, formula (5.11)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"kind\":\"engineer_formula\",\"step_id\":\"e_x\",\"expression\":\"e_x=|M_{x,base}|/V\",\"substitutions\":[{\"value\":0.0,\"unit\":\"kN*m\",\"symbol\":\"Mx_base\"},{\"value\":720.0,\"unit\":\"kN\",\"symbol\":\"V\"}],\"result\":{\"value\":0.0,\"unit\":\"m\"},\"source\":{\"engineer\":\"Аким\",\"rationale\":\"Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08.\"}},{\"step_id\":\"relative_eccentricity_x\",\"expression\":\"e/l\\\\leq1/6\",\"substitutions\":[{\"value\":0.0,\"unit\":\"1\",\"symbol\":\"e/L\"},{\"value\":1.0,\"unit\":\"1\",\"symbol\":\"numerator\"},{\"value\":6.0,\"unit\":\"1\",\"symbol\":\"denominator\"}],\"result\":{\"value\":1.0,\"unit\":\"1\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.28, applicability of formula (5.11)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"step_id\":\"pressure_diagram_x\",\"expression\":\"e<l/6\",\"substitutions\":[{\"value\":0.0,\"unit\":\"m\",\"symbol\":\"e\"},{\"value\":2.0,\"unit\":\"m\",\"symbol\":\"l\"}],\"result\":{\"value\":0.0,\"unit\":\"m\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.27, figure 5.1\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"step_id\":\"p_y_min\",\"expression\":\"p_{-}=\\\\frac{N}{A}+\\\\gamma_{mt}d-\\\\frac{M}{W}\",\"substitutions\":[{\"value\":600.0,\"unit\":\"kN\",\"symbol\":\"N\"},{\"value\":6.0,\"unit\":\"m2\",\"symbol\":\"A\"},{\"value\":20.0,\"unit\":\"kN/m3\",\"symbol\":\"gamma_mt\"},{\"value\":1.0,\"unit\":\"m\",\"symbol\":\"d\"},{\"value\":0.0,\"unit\":\"kN*m\",\"symbol\":\"M\"},{\"value\":3.0,\"unit\":\"m3\",\"symbol\":\"W\"}],\"result\":{\"value\":120.0,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.28, formula (5.11)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"step_id\":\"p_y_max\",\"expression\":\"p_{+}=\\\\frac{N}{A}+\\\\gamma_{mt}d+\\\\frac{M}{W}\",\"substitutions\":[{\"value\":600.0,\"unit\":\"kN\",\"symbol\":\"N\"},{\"value\":6.0,\"unit\":\"m2\",\"symbol\":\"A\"},{\"value\":20.0,\"unit\":\"kN/m3\",\"symbol\":\"gamma_mt\"},{\"value\":1.0,\"unit\":\"m\",\"symbol\":\"d\"},{\"value\":0.0,\"unit\":\"kN*m\",\"symbol\":\"M\"},{\"value\":3.0,\"unit\":\"m3\",\"symbol\":\"W\"}],\"result\":{\"value\":120.0,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.28, formula (5.11)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"kind\":\"engineer_formula\",\"step_id\":\"e_y\",\"expression\":\"e_y=|M_{y,base}|/V\",\"substitutions\":[{\"value\":0.0,\"unit\":\"kN*m\",\"symbol\":\"My_base\"},{\"value\":720.0,\"unit\":\"kN\",\"symbol\":\"V\"}],\"result\":{\"value\":0.0,\"unit\":\"m\"},\"source\":{\"engineer\":\"Аким\",\"rationale\":\"Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08.\"}},{\"step_id\":\"relative_eccentricity_y\",\"expression\":\"e/l\\\\leq1/6\",\"substitutions\":[{\"value\":0.0,\"unit\":\"1\",\"symbol\":\"e/L\"},{\"value\":1.0,\"unit\":\"1\",\"symbol\":\"numerator\"},{\"value\":6.0,\"unit\":\"1\",\"symbol\":\"denominator\"}],\"result\":{\"value\":1.0,\"unit\":\"1\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.28, applicability of formula (5.11)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"step_id\":\"pressure_diagram_y\",\"expression\":\"e<l/6\",\"substitutions\":[{\"value\":0.0,\"unit\":\"m\",\"symbol\":\"e\"},{\"value\":3.0,\"unit\":\"m\",\"symbol\":\"l\"}],\"result\":{\"value\":0.0,\"unit\":\"m\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.27, figure 5.1\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"step_id\":\"corner_component_pp\",\"expression\":\"P_{\\\\max}=\\\\frac{N}{A}+\\\\gamma_{mt}d+\\\\frac{M_x}{W_x}+\\\\frac{M_y}{W_y}\",\"substitutions\":[{\"value\":600.0,\"unit\":\"kN\",\"symbol\":\"N\"},{\"value\":6.0,\"unit\":\"m2\",\"symbol\":\"A\"},{\"value\":20.0,\"unit\":\"kN/m3\",\"symbol\":\"gamma_mt\"},{\"value\":1.0,\"unit\":\"m\",\"symbol\":\"d\"},{\"value\":0.0,\"unit\":\"kN*m\",\"symbol\":\"M_x\"},{\"value\":2.0,\"unit\":\"m3\",\"symbol\":\"W_x\"},{\"value\":0.0,\"unit\":\"kN*m\",\"symbol\":\"M_y\"},{\"value\":3.0,\"unit\":\"m3\",\"symbol\":\"W_y\"}],\"result\":{\"value\":120.0,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.29, formula (5.15)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"kind\":\"engineer_formula\",\"step_id\":\"p_corner_pp\",\"expression\":\"p_{pp}=p+s_x M_{x,base}/W_x+s_y M_{y,base}/W_y\",\"substitutions\":[{\"value\":120.0,\"unit\":\"kPa\",\"symbol\":\"p\"},{\"value\":0.0,\"unit\":\"kN*m\",\"symbol\":\"Mx_base\"},{\"value\":2.0,\"unit\":\"m3\",\"symbol\":\"Wx\"},{\"value\":0.0,\"unit\":\"kN*m\",\"symbol\":\"My_base\"},{\"value\":3.0,\"unit\":\"m3\",\"symbol\":\"Wy\"},{\"value\":1.0,\"unit\":\"1\",\"symbol\":\"sign_x_pp\"},{\"value\":1.0,\"unit\":\"1\",\"symbol\":\"sign_y_pp\"},{\"value\":120.0,\"unit\":\"kPa\",\"symbol\":\"corner_component_pp\"}],\"result\":{\"value\":120.0,\"unit\":\"kPa\"},\"source\":{\"engineer\":\"Аким\",\"rationale\":\"Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08.\"}},{\"step_id\":\"corner_component_pm\",\"expression\":\"P_{\\\\max}=\\\\frac{N}{A}+\\\\gamma_{mt}d+\\\\frac{M_x}{W_x}+\\\\frac{M_y}{W_y}\",\"substitutions\":[{\"value\":600.0,\"unit\":\"kN\",\"symbol\":\"N\"},{\"value\":6.0,\"unit\":\"m2\",\"symbol\":\"A\"},{\"value\":20.0,\"unit\":\"kN/m3\",\"symbol\":\"gamma_mt\"},{\"value\":1.0,\"unit\":\"m\",\"symbol\":\"d\"},{\"value\":0.0,\"unit\":\"kN*m\",\"symbol\":\"M_x\"},{\"value\":2.0,\"unit\":\"m3\",\"symbol\":\"W_x\"},{\"value\":-0.0,\"unit\":\"kN*m\",\"symbol\":\"M_y\"},{\"value\":3.0,\"unit\":\"m3\",\"symbol\":\"W_y\"}],\"result\":{\"value\":120.0,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.29, formula (5.15)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"kind\":\"engineer_formula\",\"step_id\":\"p_corner_pm\",\"expression\":\"p_{pm}=p+s_x M_{x,base}/W_x+s_y M_{y,base}/W_y\",\"substitutions\":[{\"value\":120.0,\"unit\":\"kPa\",\"symbol\":\"p\"},{\"value\":0.0,\"unit\":\"kN*m\",\"symbol\":\"Mx_base\"},{\"value\":2.0,\"unit\":\"m3\",\"symbol\":\"Wx\"},{\"value\":0.0,\"unit\":\"kN*m\",\"symbol\":\"My_base\"},{\"value\":3.0,\"unit\":\"m3\",\"symbol\":\"Wy\"},{\"value\":1.0,\"unit\":\"1\",\"symbol\":\"sign_x_pm\"},{\"value\":-1.0,\"unit\":\"1\",\"symbol\":\"sign_y_pm\"},{\"value\":120.0,\"unit\":\"kPa\",\"symbol\":\"corner_component_pm\"}],\"result\":{\"value\":120.0,\"unit\":\"kPa\"},\"source\":{\"engineer\":\"Аким\",\"rationale\":\"Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08.\"}},{\"step_id\":\"corner_component_mp\",\"expression\":\"P_{\\\\max}=\\\\frac{N}{A}+\\\\gamma_{mt}d+\\\\frac{M_x}{W_x}+\\\\frac{M_y}{W_y}\",\"substitutions\":[{\"value\":600.0,\"unit\":\"kN\",\"symbol\":\"N\"},{\"value\":6.0,\"unit\":\"m2\",\"symbol\":\"A\"},{\"value\":20.0,\"unit\":\"kN/m3\",\"symbol\":\"gamma_mt\"},{\"value\":1.0,\"unit\":\"m\",\"symbol\":\"d\"},{\"value\":-0.0,\"unit\":\"kN*m\",\"symbol\":\"M_x\"},{\"value\":2.0,\"unit\":\"m3\",\"symbol\":\"W_x\"},{\"value\":0.0,\"unit\":\"kN*m\",\"symbol\":\"M_y\"},{\"value\":3.0,\"unit\":\"m3\",\"symbol\":\"W_y\"}],\"result\":{\"value\":120.0,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.29, formula (5.15)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"kind\":\"engineer_formula\",\"step_id\":\"p_corner_mp\",\"expression\":\"p_{mp}=p+s_x M_{x,base}/W_x+s_y M_{y,base}/W_y\",\"substitutions\":[{\"value\":120.0,\"unit\":\"kPa\",\"symbol\":\"p\"},{\"value\":0.0,\"unit\":\"kN*m\",\"symbol\":\"Mx_base\"},{\"value\":2.0,\"unit\":\"m3\",\"symbol\":\"Wx\"},{\"value\":0.0,\"unit\":\"kN*m\",\"symbol\":\"My_base\"},{\"value\":3.0,\"unit\":\"m3\",\"symbol\":\"Wy\"},{\"value\":-1.0,\"unit\":\"1\",\"symbol\":\"sign_x_mp\"},{\"value\":1.0,\"unit\":\"1\",\"symbol\":\"sign_y_mp\"},{\"value\":120.0,\"unit\":\"kPa\",\"symbol\":\"corner_component_mp\"}],\"result\":{\"value\":120.0,\"unit\":\"kPa\"},\"source\":{\"engineer\":\"Аким\",\"rationale\":\"Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08.\"}},{\"step_id\":\"corner_component_mm\",\"expression\":\"P_{\\\\max}=\\\\frac{N}{A}+\\\\gamma_{mt}d+\\\\frac{M_x}{W_x}+\\\\frac{M_y}{W_y}\",\"substitutions\":[{\"value\":600.0,\"unit\":\"kN\",\"symbol\":\"N\"},{\"value\":6.0,\"unit\":\"m2\",\"symbol\":\"A\"},{\"value\":20.0,\"unit\":\"kN/m3\",\"symbol\":\"gamma_mt\"},{\"value\":1.0,\"unit\":\"m\",\"symbol\":\"d\"},{\"value\":-0.0,\"unit\":\"kN*m\",\"symbol\":\"M_x\"},{\"value\":2.0,\"unit\":\"m3\",\"symbol\":\"W_x\"},{\"value\":-0.0,\"unit\":\"kN*m\",\"symbol\":\"M_y\"},{\"value\":3.0,\"unit\":\"m3\",\"symbol\":\"W_y\"}],\"result\":{\"value\":120.0,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.29, formula (5.15)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"kind\":\"engineer_formula\",\"step_id\":\"p_corner_mm\",\"expression\":\"p_{mm}=p+s_x M_{x,base}/W_x+s_y M_{y,base}/W_y\",\"substitutions\":[{\"value\":120.0,\"unit\":\"kPa\",\"symbol\":\"p\"},{\"value\":0.0,\"unit\":\"kN*m\",\"symbol\":\"Mx_base\"},{\"value\":2.0,\"unit\":\"m3\",\"symbol\":\"Wx\"},{\"value\":0.0,\"unit\":\"kN*m\",\"symbol\":\"My_base\"},{\"value\":3.0,\"unit\":\"m3\",\"symbol\":\"Wy\"},{\"value\":-1.0,\"unit\":\"1\",\"symbol\":\"sign_x_mm\"},{\"value\":-1.0,\"unit\":\"1\",\"symbol\":\"sign_y_mm\"},{\"value\":120.0,\"unit\":\"kPa\",\"symbol\":\"corner_component_mm\"}],\"result\":{\"value\":120.0,\"unit\":\"kPa\"},\"source\":{\"engineer\":\"Аким\",\"rationale\":\"Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08.\"}},{\"kind\":\"engineer_formula\",\"step_id\":\"p_corner_min\",\"expression\":\"p_{corner,min}=\\\\min(p_{++},p_{+-},p_{-+},p_{--})\",\"substitutions\":[{\"value\":120.0,\"unit\":\"kPa\",\"symbol\":\"p_corner_pp\"},{\"value\":120.0,\"unit\":\"kPa\",\"symbol\":\"p_corner_pm\"},{\"value\":120.0,\"unit\":\"kPa\",\"symbol\":\"p_corner_mp\"},{\"value\":120.0,\"unit\":\"kPa\",\"symbol\":\"p_corner_mm\"}],\"result\":{\"value\":120.0,\"unit\":\"kPa\"},\"source\":{\"engineer\":\"Аким\",\"rationale\":\"Полный контакт прямоугольной подошвы: минимум четырёх подписанных угловых давлений неотрицателен; решение инженера 2026-11-08.\"}},{\"kind\":\"engineer_formula\",\"step_id\":\"p_corner_max\",\"expression\":\"p_{corner,max}=\\\\max(p_{++},p_{+-},p_{-+},p_{--})\",\"substitutions\":[{\"value\":120.0,\"unit\":\"kPa\",\"symbol\":\"p_corner_pp\"},{\"value\":120.0,\"unit\":\"kPa\",\"symbol\":\"p_corner_pm\"},{\"value\":120.0,\"unit\":\"kPa\",\"symbol\":\"p_corner_mp\"},{\"value\":120.0,\"unit\":\"kPa\",\"symbol\":\"p_corner_mm\"}],\"result\":{\"value\":120.0,\"unit\":\"kPa\"},\"source\":{\"engineer\":\"Аким\",\"rationale\":\"Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08.\"}},{\"step_id\":\"edge_limit_multiplier\",\"expression\":\"edge_limit_multiplier\",\"substitutions\":[],\"result\":{\"value\":1.2,\"unit\":\"1\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.26\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"table\"},{\"step_id\":\"edge_limit\",\"expression\":\"p_{edge,lim}=\\\\lambda_e R\",\"substitutions\":[{\"value\":1.2,\"unit\":\"1\",\"symbol\":\"edge_limit_multiplier\"},{\"value\":152.02,\"unit\":\"kPa\",\"symbol\":\"R\"}],\"result\":{\"value\":182.424,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.26\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"step_id\":\"corner_limit_multiplier\",\"expression\":\"corner_limit_multiplier\",\"substitutions\":[],\"result\":{\"value\":1.5,\"unit\":\"1\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.26\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"table\"},{\"step_id\":\"corner_limit\",\"expression\":\"p_{corner,lim}=\\\\lambda_c R\",\"substitutions\":[{\"value\":1.5,\"unit\":\"1\",\"symbol\":\"corner_limit_multiplier\"},{\"value\":152.02,\"unit\":\"kPa\",\"symbol\":\"R\"}],\"result\":{\"value\":228.03000000000003,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.26\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"step_id\":\"p_le_R\",\"expression\":\"p \\\\le R\",\"substitutions\":[{\"value\":120.0,\"unit\":\"kPa\",\"symbol\":\"p\"},{\"value\":152.02,\"unit\":\"kPa\",\"symbol\":\"R\"}],\"result\":{\"value\":120.0,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"check\",\"operator\":\"le\",\"right\":{\"value\":152.02,\"unit\":\"kPa\"},\"passed\":true},{\"step_id\":\"p_x_max_le_limit\",\"expression\":\"p_x_max \\\\le edge_limit\",\"substitutions\":[{\"value\":120.0,\"unit\":\"kPa\",\"symbol\":\"p_x_max\"},{\"value\":182.424,\"unit\":\"kPa\",\"symbol\":\"edge_limit\"}],\"result\":{\"value\":120.0,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.26\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"check\",\"operator\":\"le\",\"right\":{\"value\":182.424,\"unit\":\"kPa\"},\"passed\":true},{\"step_id\":\"p_y_max_le_limit\",\"expression\":\"p_y_max \\\\le edge_limit\",\"substitutions\":[{\"value\":120.0,\"unit\":\"kPa\",\"symbol\":\"p_y_max\"},{\"value\":182.424,\"unit\":\"kPa\",\"symbol\":\"edge_limit\"}],\"result\":{\"value\":120.0,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.26\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"check\",\"operator\":\"le\",\"right\":{\"value\":182.424,\"unit\":\"kPa\"},\"passed\":true},{\"step_id\":\"p_corner_max_le_limit\",\"expression\":\"p_corner_max \\\\le corner_limit\",\"substitutions\":[{\"value\":120.0,\"unit\":\"kPa\",\"symbol\":\"p_corner_max\"},{\"value\":228.03000000000003,\"unit\":\"kPa\",\"symbol\":\"corner_limit\"}],\"result\":{\"value\":120.0,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.26\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"check\",\"operator\":\"le\",\"right\":{\"value\":228.03000000000003,\"unit\":\"kPa\"},\"passed\":true}],\"unverified_step_count\":30,\"result_id\":\"55555555-5555-4555-8555-555555555555\",\"parameter_source\":{\"kind\":\"interim\",\"data_sha256\":\"faaa0724af57ca6c8066f558c4e75c2785d099b34cbfb07c4a85892fdc3b68fe\",\"profile\":\"strict\"}}"

export const LOADS_ONE_AXIS_ID = '66666666-6666-4666-8666-666666666666'

export const loadsOneAxisInputs = {
  "b": {
    "value": 2,
    "unit": "m"
  },
  "d_1": {
    "value": 1,
    "unit": "m"
  },
  "d_b": {
    "value": 0,
    "unit": "m"
  },
  "gamma_II": {
    "value": 20,
    "unit": "kN/m3"
  },
  "gamma_II_prime": {
    "value": 20,
    "unit": "kN/m3"
  },
  "c_II": {
    "value": 10,
    "unit": "kPa"
  },
  "phi_II": {
    "value": 20,
    "unit": "deg"
  },
  "l": {
    "value": 3,
    "unit": "m"
  },
  "h": {
    "value": 1,
    "unit": "m"
  },
  "d": {
    "value": 1,
    "unit": "m"
  },
  "N": {
    "value": 600,
    "unit": "kN"
  },
  "Mx": {
    "value": 40,
    "unit": "kN*m"
  },
  "My": {
    "value": 0,
    "unit": "kN*m"
  },
  "Qx": {
    "value": 20,
    "unit": "kN"
  },
  "Qy": {
    "value": 0,
    "unit": "kN"
  }
} satisfies CalculationRequest['inputs']

export const loadsOneAxisEnvelope = {
  "engine_version": "0.1.0",
  "input_hash": "598e8b96843dbd2bf854325e7e09b3d16e85b58e54d9057402f6fb2e6932a1c0", // pragma: allowlist secret
  "outputs": [
    {
      "value": 152.02,
      "unit": "kPa",
      "quantity": "R",
      "rounding_rule": {
        "decimals": 2,
        "mode": "half_up"
      },
      "rounding_source": {
        "engineer": "Аким",
        "rationale": "Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются."
      }
    },
    {
      "value": 120.0,
      "unit": "kPa",
      "quantity": "p",
      "rounding_rule": {
        "decimals": 2,
        "mode": "half_up"
      },
      "rounding_source": {
        "engineer": "Аким",
        "rationale": "Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются."
      }
    },
    {
      "value": 90.0,
      "unit": "kPa",
      "quantity": "p_x_min",
      "rounding_rule": {
        "decimals": 2,
        "mode": "half_up"
      },
      "rounding_source": {
        "engineer": "Аким",
        "rationale": "Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются."
      }
    },
    {
      "value": 150.0,
      "unit": "kPa",
      "quantity": "p_x_max",
      "rounding_rule": {
        "decimals": 2,
        "mode": "half_up"
      },
      "rounding_source": {
        "engineer": "Аким",
        "rationale": "Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются."
      }
    },
    {
      "value": 120.0,
      "unit": "kPa",
      "quantity": "p_y_min",
      "rounding_rule": {
        "decimals": 2,
        "mode": "half_up"
      },
      "rounding_source": {
        "engineer": "Аким",
        "rationale": "Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются."
      }
    },
    {
      "value": 120.0,
      "unit": "kPa",
      "quantity": "p_y_max",
      "rounding_rule": {
        "decimals": 2,
        "mode": "half_up"
      },
      "rounding_source": {
        "engineer": "Аким",
        "rationale": "Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются."
      }
    },
    {
      "value": 150.0,
      "unit": "kPa",
      "quantity": "p_corner_pp",
      "rounding_rule": {
        "decimals": 2,
        "mode": "half_up"
      },
      "rounding_source": {
        "engineer": "Аким",
        "rationale": "Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются."
      }
    },
    {
      "value": 150.0,
      "unit": "kPa",
      "quantity": "p_corner_pm",
      "rounding_rule": {
        "decimals": 2,
        "mode": "half_up"
      },
      "rounding_source": {
        "engineer": "Аким",
        "rationale": "Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются."
      }
    },
    {
      "value": 90.0,
      "unit": "kPa",
      "quantity": "p_corner_mp",
      "rounding_rule": {
        "decimals": 2,
        "mode": "half_up"
      },
      "rounding_source": {
        "engineer": "Аким",
        "rationale": "Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются."
      }
    },
    {
      "value": 90.0,
      "unit": "kPa",
      "quantity": "p_corner_mm",
      "rounding_rule": {
        "decimals": 2,
        "mode": "half_up"
      },
      "rounding_source": {
        "engineer": "Аким",
        "rationale": "Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются."
      }
    }
  ],
  "norm_refs": [
    {
      "document": "СП 22.13330.2016",
      "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
      "clause": "5.6.7, таблица 5.4",
      "status": "unverified",
      "provenance": "machine-extracted"
    },
    {
      "document": "СП 22.13330.2016",
      "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
      "clause": "5.6.7, экспликация k",
      "status": "unverified",
      "provenance": "machine-extracted"
    },
    {
      "document": "СП 22.13330.2016",
      "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
      "clause": "5.6.7, таблица 5.5",
      "status": "unverified",
      "provenance": "machine-extracted"
    },
    {
      "document": "СП 22.13330.2016",
      "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
      "clause": "5.6.7, экспликация k_z",
      "status": "unverified",
      "provenance": "machine-extracted"
    },
    {
      "document": "СП 22.13330.2016",
      "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
      "clause": "5.6.7, формула (5.7)",
      "status": "unverified",
      "provenance": "machine-extracted"
    },
    {
      "document": "СП 22.13330.2016",
      "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
      "clause": "5.6.28, explanation of formula (5.11)",
      "status": "unverified",
      "provenance": "machine-extracted"
    },
    {
      "document": "СП 22.13330.2016",
      "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
      "clause": "5.6.28, formula (5.11)",
      "status": "unverified",
      "provenance": "machine-extracted"
    },
    {
      "document": "СП 22.13330.2016",
      "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
      "clause": "5.6.28, applicability of formula (5.11)",
      "status": "unverified",
      "provenance": "machine-extracted"
    },
    {
      "document": "СП 22.13330.2016",
      "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
      "clause": "5.6.27, figure 5.1",
      "status": "unverified",
      "provenance": "machine-extracted"
    },
    {
      "document": "СП 22.13330.2016",
      "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
      "clause": "5.6.29, formula (5.15)",
      "status": "unverified",
      "provenance": "machine-extracted"
    },
    {
      "document": "СП 22.13330.2016",
      "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
      "clause": "5.6.26",
      "status": "unverified",
      "provenance": "machine-extracted"
    },
    {
      "document": "СП 22.13330.2016",
      "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
      "clause": "5.6.7",
      "status": "unverified",
      "provenance": "machine-extracted"
    }
  ],
  "engineer_rules": [
    {
      "engineer": "Аким",
      "rationale": "Геометрия прямоугольной подошвы: A=b*l, Wx=l*b²/6, Wy=b*l²/6; инженерный контракт 2026-11-08."
    },
    {
      "engineer": "Аким",
      "rationale": "Подписанный перенос нагрузок к подошве M_base=M+Q*h; оси x=b и y=l; инженерный контракт 2026-11-08."
    },
    {
      "engineer": "Аким",
      "rationale": "Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08."
    },
    {
      "engineer": "Аким",
      "rationale": "Полный контакт прямоугольной подошвы: минимум четырёх подписанных угловых давлений неотрицателен; решение инженера 2026-11-08."
    },
    {
      "engineer": "Аким",
      "rationale": "Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются."
    }
  ],
  "verdict": "pass",
  "verdict_reason": {
    "kind": "check",
    "step_id": "p_corner_max_le_limit"
  },
  "warnings": [],
  "trace": [
    {
      "step_id": "gamma_c1",
      "expression": "\\gamma_{c1}",
      "substitutions": [],
      "result": {
        "value": 1.1,
        "unit": "1"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.7, таблица 5.4",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "table"
    },
    {
      "step_id": "gamma_c2",
      "expression": "\\gamma_{c2}",
      "substitutions": [],
      "result": {
        "value": 1.0,
        "unit": "1"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.7, таблица 5.4",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "table"
    },
    {
      "step_id": "k",
      "expression": "k",
      "substitutions": [],
      "result": {
        "value": 1.0,
        "unit": "1"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.7, экспликация k",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "table"
    },
    {
      "step_id": "M_gamma",
      "expression": "M_{\\gamma} = M_{\\gamma}\\left(\\varphi_{II}\\right)",
      "substitutions": [
        {
          "value": 20.0,
          "unit": "deg",
          "symbol": "phi_II"
        }
      ],
      "result": {
        "value": 0.51,
        "unit": "1"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.7, таблица 5.5",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "table"
    },
    {
      "step_id": "M_q",
      "expression": "M_{q} = M_{q}\\left(\\varphi_{II}\\right)",
      "substitutions": [
        {
          "value": 20.0,
          "unit": "deg",
          "symbol": "phi_II"
        }
      ],
      "result": {
        "value": 3.06,
        "unit": "1"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.7, таблица 5.5",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "table"
    },
    {
      "step_id": "M_c",
      "expression": "M_{c} = M_{c}\\left(\\varphi_{II}\\right)",
      "substitutions": [
        {
          "value": 20.0,
          "unit": "deg",
          "symbol": "phi_II"
        }
      ],
      "result": {
        "value": 5.66,
        "unit": "1"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.7, таблица 5.5",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "table"
    },
    {
      "step_id": "k_z",
      "expression": "k_{z}=1",
      "substitutions": [],
      "result": {
        "value": 1.0,
        "unit": "1"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.7, экспликация k_z",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "step_id": "R",
      "expression": "R=\\frac{\\gamma_{c1}\\gamma_{c2}}{k}\\left[M_{\\gamma}k_{z}b\\gamma_{II}+M_{q}d_{1}\\gamma'_{II}+(M_{q}-1)d_{b}\\gamma'_{II}+M_{c}c_{II}\\right]",
      "substitutions": [
        {
          "value": 1.1,
          "unit": "1",
          "symbol": "gamma_c1"
        },
        {
          "value": 1.0,
          "unit": "1",
          "symbol": "gamma_c2"
        },
        {
          "value": 1.0,
          "unit": "1",
          "symbol": "k"
        },
        {
          "value": 0.51,
          "unit": "1",
          "symbol": "M_gamma"
        },
        {
          "value": 1.0,
          "unit": "1",
          "symbol": "k_z"
        },
        {
          "value": 2.0,
          "unit": "m",
          "symbol": "b"
        },
        {
          "value": 20.0,
          "unit": "kN/m3",
          "symbol": "gamma_II"
        },
        {
          "value": 3.06,
          "unit": "1",
          "symbol": "M_q"
        },
        {
          "value": 1.0,
          "unit": "m",
          "symbol": "d_1"
        },
        {
          "value": 20.0,
          "unit": "kN/m3",
          "symbol": "gamma_II_prime"
        },
        {
          "value": 0.0,
          "unit": "m",
          "symbol": "d_b"
        },
        {
          "value": 5.66,
          "unit": "1",
          "symbol": "M_c"
        },
        {
          "value": 10.0,
          "unit": "kPa",
          "symbol": "c_II"
        }
      ],
      "result": {
        "value": 152.02,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.7, формула (5.7)",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "kind": "engineer_formula",
      "step_id": "A",
      "expression": "A=b l",
      "substitutions": [
        {
          "value": 2.0,
          "unit": "m",
          "symbol": "b"
        },
        {
          "value": 3.0,
          "unit": "m",
          "symbol": "l"
        }
      ],
      "result": {
        "value": 6.0,
        "unit": "m2"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Геометрия прямоугольной подошвы: A=b*l, Wx=l*b²/6, Wy=b*l²/6; инженерный контракт 2026-11-08."
      }
    },
    {
      "kind": "engineer_formula",
      "step_id": "Wx",
      "expression": "W_x=l b^2/6",
      "substitutions": [
        {
          "value": 2.0,
          "unit": "m",
          "symbol": "b"
        },
        {
          "value": 3.0,
          "unit": "m",
          "symbol": "l"
        }
      ],
      "result": {
        "value": 2.0,
        "unit": "m3"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Геометрия прямоугольной подошвы: A=b*l, Wx=l*b²/6, Wy=b*l²/6; инженерный контракт 2026-11-08."
      }
    },
    {
      "kind": "engineer_formula",
      "step_id": "Wy",
      "expression": "W_y=b l^2/6",
      "substitutions": [
        {
          "value": 2.0,
          "unit": "m",
          "symbol": "b"
        },
        {
          "value": 3.0,
          "unit": "m",
          "symbol": "l"
        }
      ],
      "result": {
        "value": 3.0,
        "unit": "m3"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Геометрия прямоугольной подошвы: A=b*l, Wx=l*b²/6, Wy=b*l²/6; инженерный контракт 2026-11-08."
      }
    },
    {
      "kind": "engineer_formula",
      "step_id": "Mx_base",
      "expression": "M_{x,base}=M_x+Q_x h",
      "substitutions": [
        {
          "value": 40.0,
          "unit": "kN*m",
          "symbol": "Mx"
        },
        {
          "value": 20.0,
          "unit": "kN",
          "symbol": "Qx"
        },
        {
          "value": 1.0,
          "unit": "m",
          "symbol": "h"
        }
      ],
      "result": {
        "value": 60.0,
        "unit": "kN*m"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Подписанный перенос нагрузок к подошве M_base=M+Q*h; оси x=b и y=l; инженерный контракт 2026-11-08."
      }
    },
    {
      "kind": "engineer_formula",
      "step_id": "My_base",
      "expression": "M_{y,base}=M_y+Q_y h",
      "substitutions": [
        {
          "value": 0.0,
          "unit": "kN*m",
          "symbol": "My"
        },
        {
          "value": 0.0,
          "unit": "kN",
          "symbol": "Qy"
        },
        {
          "value": 1.0,
          "unit": "m",
          "symbol": "h"
        }
      ],
      "result": {
        "value": 0.0,
        "unit": "kN*m"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Подписанный перенос нагрузок к подошве M_base=M+Q*h; оси x=b и y=l; инженерный контракт 2026-11-08."
      }
    },
    {
      "step_id": "gamma_mt",
      "expression": "\\gamma_{mt}",
      "substitutions": [],
      "result": {
        "value": 20.0,
        "unit": "kN/m3"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.28, explanation of formula (5.11)",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "table"
    },
    {
      "step_id": "p",
      "expression": "p_{+}=\\frac{N}{A}+\\gamma_{mt}d+\\frac{M}{W}",
      "substitutions": [
        {
          "value": 600.0,
          "unit": "kN",
          "symbol": "N"
        },
        {
          "value": 6.0,
          "unit": "m2",
          "symbol": "A"
        },
        {
          "value": 20.0,
          "unit": "kN/m3",
          "symbol": "gamma_mt"
        },
        {
          "value": 1.0,
          "unit": "m",
          "symbol": "d"
        },
        {
          "value": 0.0,
          "unit": "kN*m",
          "symbol": "M"
        },
        {
          "value": 2.0,
          "unit": "m3",
          "symbol": "W"
        }
      ],
      "result": {
        "value": 120.0,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.28, formula (5.11)",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "kind": "engineer_formula",
      "step_id": "V",
      "expression": "V=N+\\gamma_{mt} d A",
      "substitutions": [
        {
          "value": 600.0,
          "unit": "kN",
          "symbol": "N"
        },
        {
          "value": 20.0,
          "unit": "kN/m3",
          "symbol": "gamma_mt"
        },
        {
          "value": 1.0,
          "unit": "m",
          "symbol": "d"
        },
        {
          "value": 6.0,
          "unit": "m2",
          "symbol": "A"
        }
      ],
      "result": {
        "value": 720.0,
        "unit": "kN"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08."
      }
    },
    {
      "step_id": "p_x_min",
      "expression": "p_{-}=\\frac{N}{A}+\\gamma_{mt}d-\\frac{M}{W}",
      "substitutions": [
        {
          "value": 600.0,
          "unit": "kN",
          "symbol": "N"
        },
        {
          "value": 6.0,
          "unit": "m2",
          "symbol": "A"
        },
        {
          "value": 20.0,
          "unit": "kN/m3",
          "symbol": "gamma_mt"
        },
        {
          "value": 1.0,
          "unit": "m",
          "symbol": "d"
        },
        {
          "value": 60.0,
          "unit": "kN*m",
          "symbol": "M"
        },
        {
          "value": 2.0,
          "unit": "m3",
          "symbol": "W"
        }
      ],
      "result": {
        "value": 90.0,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.28, formula (5.11)",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "step_id": "p_x_max",
      "expression": "p_{+}=\\frac{N}{A}+\\gamma_{mt}d+\\frac{M}{W}",
      "substitutions": [
        {
          "value": 600.0,
          "unit": "kN",
          "symbol": "N"
        },
        {
          "value": 6.0,
          "unit": "m2",
          "symbol": "A"
        },
        {
          "value": 20.0,
          "unit": "kN/m3",
          "symbol": "gamma_mt"
        },
        {
          "value": 1.0,
          "unit": "m",
          "symbol": "d"
        },
        {
          "value": 60.0,
          "unit": "kN*m",
          "symbol": "M"
        },
        {
          "value": 2.0,
          "unit": "m3",
          "symbol": "W"
        }
      ],
      "result": {
        "value": 150.0,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.28, formula (5.11)",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "kind": "engineer_formula",
      "step_id": "e_x",
      "expression": "e_x=|M_{x,base}|/V",
      "substitutions": [
        {
          "value": 60.0,
          "unit": "kN*m",
          "symbol": "Mx_base"
        },
        {
          "value": 720.0,
          "unit": "kN",
          "symbol": "V"
        }
      ],
      "result": {
        "value": 0.08333333333333333,
        "unit": "m"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08."
      }
    },
    {
      "step_id": "relative_eccentricity_x",
      "expression": "e/l\\leq1/6",
      "substitutions": [
        {
          "value": 0.041666666666666664,
          "unit": "1",
          "symbol": "e/L"
        },
        {
          "value": 1.0,
          "unit": "1",
          "symbol": "numerator"
        },
        {
          "value": 6.0,
          "unit": "1",
          "symbol": "denominator"
        }
      ],
      "result": {
        "value": 1.0,
        "unit": "1"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.28, applicability of formula (5.11)",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "step_id": "pressure_diagram_x",
      "expression": "e<l/6",
      "substitutions": [
        {
          "value": 0.08333333333333333,
          "unit": "m",
          "symbol": "e"
        },
        {
          "value": 2.0,
          "unit": "m",
          "symbol": "l"
        }
      ],
      "result": {
        "value": 0.08333333333333333,
        "unit": "m"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.27, figure 5.1",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "step_id": "p_y_min",
      "expression": "p_{-}=\\frac{N}{A}+\\gamma_{mt}d-\\frac{M}{W}",
      "substitutions": [
        {
          "value": 600.0,
          "unit": "kN",
          "symbol": "N"
        },
        {
          "value": 6.0,
          "unit": "m2",
          "symbol": "A"
        },
        {
          "value": 20.0,
          "unit": "kN/m3",
          "symbol": "gamma_mt"
        },
        {
          "value": 1.0,
          "unit": "m",
          "symbol": "d"
        },
        {
          "value": 0.0,
          "unit": "kN*m",
          "symbol": "M"
        },
        {
          "value": 3.0,
          "unit": "m3",
          "symbol": "W"
        }
      ],
      "result": {
        "value": 120.0,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.28, formula (5.11)",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "step_id": "p_y_max",
      "expression": "p_{+}=\\frac{N}{A}+\\gamma_{mt}d+\\frac{M}{W}",
      "substitutions": [
        {
          "value": 600.0,
          "unit": "kN",
          "symbol": "N"
        },
        {
          "value": 6.0,
          "unit": "m2",
          "symbol": "A"
        },
        {
          "value": 20.0,
          "unit": "kN/m3",
          "symbol": "gamma_mt"
        },
        {
          "value": 1.0,
          "unit": "m",
          "symbol": "d"
        },
        {
          "value": 0.0,
          "unit": "kN*m",
          "symbol": "M"
        },
        {
          "value": 3.0,
          "unit": "m3",
          "symbol": "W"
        }
      ],
      "result": {
        "value": 120.0,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.28, formula (5.11)",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "kind": "engineer_formula",
      "step_id": "e_y",
      "expression": "e_y=|M_{y,base}|/V",
      "substitutions": [
        {
          "value": 0.0,
          "unit": "kN*m",
          "symbol": "My_base"
        },
        {
          "value": 720.0,
          "unit": "kN",
          "symbol": "V"
        }
      ],
      "result": {
        "value": 0.0,
        "unit": "m"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08."
      }
    },
    {
      "step_id": "relative_eccentricity_y",
      "expression": "e/l\\leq1/6",
      "substitutions": [
        {
          "value": 0.0,
          "unit": "1",
          "symbol": "e/L"
        },
        {
          "value": 1.0,
          "unit": "1",
          "symbol": "numerator"
        },
        {
          "value": 6.0,
          "unit": "1",
          "symbol": "denominator"
        }
      ],
      "result": {
        "value": 1.0,
        "unit": "1"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.28, applicability of formula (5.11)",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "step_id": "pressure_diagram_y",
      "expression": "e<l/6",
      "substitutions": [
        {
          "value": 0.0,
          "unit": "m",
          "symbol": "e"
        },
        {
          "value": 3.0,
          "unit": "m",
          "symbol": "l"
        }
      ],
      "result": {
        "value": 0.0,
        "unit": "m"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.27, figure 5.1",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "step_id": "corner_component_pp",
      "expression": "P_{\\max}=\\frac{N}{A}+\\gamma_{mt}d+\\frac{M_x}{W_x}+\\frac{M_y}{W_y}",
      "substitutions": [
        {
          "value": 600.0,
          "unit": "kN",
          "symbol": "N"
        },
        {
          "value": 6.0,
          "unit": "m2",
          "symbol": "A"
        },
        {
          "value": 20.0,
          "unit": "kN/m3",
          "symbol": "gamma_mt"
        },
        {
          "value": 1.0,
          "unit": "m",
          "symbol": "d"
        },
        {
          "value": 60.0,
          "unit": "kN*m",
          "symbol": "M_x"
        },
        {
          "value": 2.0,
          "unit": "m3",
          "symbol": "W_x"
        },
        {
          "value": 0.0,
          "unit": "kN*m",
          "symbol": "M_y"
        },
        {
          "value": 3.0,
          "unit": "m3",
          "symbol": "W_y"
        }
      ],
      "result": {
        "value": 150.0,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.29, formula (5.15)",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "kind": "engineer_formula",
      "step_id": "p_corner_pp",
      "expression": "p_{pp}=p+s_x M_{x,base}/W_x+s_y M_{y,base}/W_y",
      "substitutions": [
        {
          "value": 120.0,
          "unit": "kPa",
          "symbol": "p"
        },
        {
          "value": 60.0,
          "unit": "kN*m",
          "symbol": "Mx_base"
        },
        {
          "value": 2.0,
          "unit": "m3",
          "symbol": "Wx"
        },
        {
          "value": 0.0,
          "unit": "kN*m",
          "symbol": "My_base"
        },
        {
          "value": 3.0,
          "unit": "m3",
          "symbol": "Wy"
        },
        {
          "value": 1.0,
          "unit": "1",
          "symbol": "sign_x_pp"
        },
        {
          "value": 1.0,
          "unit": "1",
          "symbol": "sign_y_pp"
        },
        {
          "value": 150.0,
          "unit": "kPa",
          "symbol": "corner_component_pp"
        }
      ],
      "result": {
        "value": 150.0,
        "unit": "kPa"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08."
      }
    },
    {
      "step_id": "corner_component_pm",
      "expression": "P_{\\max}=\\frac{N}{A}+\\gamma_{mt}d+\\frac{M_x}{W_x}+\\frac{M_y}{W_y}",
      "substitutions": [
        {
          "value": 600.0,
          "unit": "kN",
          "symbol": "N"
        },
        {
          "value": 6.0,
          "unit": "m2",
          "symbol": "A"
        },
        {
          "value": 20.0,
          "unit": "kN/m3",
          "symbol": "gamma_mt"
        },
        {
          "value": 1.0,
          "unit": "m",
          "symbol": "d"
        },
        {
          "value": 60.0,
          "unit": "kN*m",
          "symbol": "M_x"
        },
        {
          "value": 2.0,
          "unit": "m3",
          "symbol": "W_x"
        },
        {
          "value": -0.0,
          "unit": "kN*m",
          "symbol": "M_y"
        },
        {
          "value": 3.0,
          "unit": "m3",
          "symbol": "W_y"
        }
      ],
      "result": {
        "value": 150.0,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.29, formula (5.15)",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "kind": "engineer_formula",
      "step_id": "p_corner_pm",
      "expression": "p_{pm}=p+s_x M_{x,base}/W_x+s_y M_{y,base}/W_y",
      "substitutions": [
        {
          "value": 120.0,
          "unit": "kPa",
          "symbol": "p"
        },
        {
          "value": 60.0,
          "unit": "kN*m",
          "symbol": "Mx_base"
        },
        {
          "value": 2.0,
          "unit": "m3",
          "symbol": "Wx"
        },
        {
          "value": 0.0,
          "unit": "kN*m",
          "symbol": "My_base"
        },
        {
          "value": 3.0,
          "unit": "m3",
          "symbol": "Wy"
        },
        {
          "value": 1.0,
          "unit": "1",
          "symbol": "sign_x_pm"
        },
        {
          "value": -1.0,
          "unit": "1",
          "symbol": "sign_y_pm"
        },
        {
          "value": 150.0,
          "unit": "kPa",
          "symbol": "corner_component_pm"
        }
      ],
      "result": {
        "value": 150.0,
        "unit": "kPa"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08."
      }
    },
    {
      "step_id": "corner_component_mp",
      "expression": "P_{\\max}=\\frac{N}{A}+\\gamma_{mt}d+\\frac{M_x}{W_x}+\\frac{M_y}{W_y}",
      "substitutions": [
        {
          "value": 600.0,
          "unit": "kN",
          "symbol": "N"
        },
        {
          "value": 6.0,
          "unit": "m2",
          "symbol": "A"
        },
        {
          "value": 20.0,
          "unit": "kN/m3",
          "symbol": "gamma_mt"
        },
        {
          "value": 1.0,
          "unit": "m",
          "symbol": "d"
        },
        {
          "value": -60.0,
          "unit": "kN*m",
          "symbol": "M_x"
        },
        {
          "value": 2.0,
          "unit": "m3",
          "symbol": "W_x"
        },
        {
          "value": 0.0,
          "unit": "kN*m",
          "symbol": "M_y"
        },
        {
          "value": 3.0,
          "unit": "m3",
          "symbol": "W_y"
        }
      ],
      "result": {
        "value": 90.0,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.29, formula (5.15)",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "kind": "engineer_formula",
      "step_id": "p_corner_mp",
      "expression": "p_{mp}=p+s_x M_{x,base}/W_x+s_y M_{y,base}/W_y",
      "substitutions": [
        {
          "value": 120.0,
          "unit": "kPa",
          "symbol": "p"
        },
        {
          "value": 60.0,
          "unit": "kN*m",
          "symbol": "Mx_base"
        },
        {
          "value": 2.0,
          "unit": "m3",
          "symbol": "Wx"
        },
        {
          "value": 0.0,
          "unit": "kN*m",
          "symbol": "My_base"
        },
        {
          "value": 3.0,
          "unit": "m3",
          "symbol": "Wy"
        },
        {
          "value": -1.0,
          "unit": "1",
          "symbol": "sign_x_mp"
        },
        {
          "value": 1.0,
          "unit": "1",
          "symbol": "sign_y_mp"
        },
        {
          "value": 90.0,
          "unit": "kPa",
          "symbol": "corner_component_mp"
        }
      ],
      "result": {
        "value": 90.0,
        "unit": "kPa"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08."
      }
    },
    {
      "step_id": "corner_component_mm",
      "expression": "P_{\\max}=\\frac{N}{A}+\\gamma_{mt}d+\\frac{M_x}{W_x}+\\frac{M_y}{W_y}",
      "substitutions": [
        {
          "value": 600.0,
          "unit": "kN",
          "symbol": "N"
        },
        {
          "value": 6.0,
          "unit": "m2",
          "symbol": "A"
        },
        {
          "value": 20.0,
          "unit": "kN/m3",
          "symbol": "gamma_mt"
        },
        {
          "value": 1.0,
          "unit": "m",
          "symbol": "d"
        },
        {
          "value": -60.0,
          "unit": "kN*m",
          "symbol": "M_x"
        },
        {
          "value": 2.0,
          "unit": "m3",
          "symbol": "W_x"
        },
        {
          "value": -0.0,
          "unit": "kN*m",
          "symbol": "M_y"
        },
        {
          "value": 3.0,
          "unit": "m3",
          "symbol": "W_y"
        }
      ],
      "result": {
        "value": 90.0,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.29, formula (5.15)",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "kind": "engineer_formula",
      "step_id": "p_corner_mm",
      "expression": "p_{mm}=p+s_x M_{x,base}/W_x+s_y M_{y,base}/W_y",
      "substitutions": [
        {
          "value": 120.0,
          "unit": "kPa",
          "symbol": "p"
        },
        {
          "value": 60.0,
          "unit": "kN*m",
          "symbol": "Mx_base"
        },
        {
          "value": 2.0,
          "unit": "m3",
          "symbol": "Wx"
        },
        {
          "value": 0.0,
          "unit": "kN*m",
          "symbol": "My_base"
        },
        {
          "value": 3.0,
          "unit": "m3",
          "symbol": "Wy"
        },
        {
          "value": -1.0,
          "unit": "1",
          "symbol": "sign_x_mm"
        },
        {
          "value": -1.0,
          "unit": "1",
          "symbol": "sign_y_mm"
        },
        {
          "value": 90.0,
          "unit": "kPa",
          "symbol": "corner_component_mm"
        }
      ],
      "result": {
        "value": 90.0,
        "unit": "kPa"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08."
      }
    },
    {
      "kind": "engineer_formula",
      "step_id": "p_corner_min",
      "expression": "p_{corner,min}=\\min(p_{++},p_{+-},p_{-+},p_{--})",
      "substitutions": [
        {
          "value": 150.0,
          "unit": "kPa",
          "symbol": "p_corner_pp"
        },
        {
          "value": 150.0,
          "unit": "kPa",
          "symbol": "p_corner_pm"
        },
        {
          "value": 90.0,
          "unit": "kPa",
          "symbol": "p_corner_mp"
        },
        {
          "value": 90.0,
          "unit": "kPa",
          "symbol": "p_corner_mm"
        }
      ],
      "result": {
        "value": 90.0,
        "unit": "kPa"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Полный контакт прямоугольной подошвы: минимум четырёх подписанных угловых давлений неотрицателен; решение инженера 2026-11-08."
      }
    },
    {
      "kind": "engineer_formula",
      "step_id": "p_corner_max",
      "expression": "p_{corner,max}=\\max(p_{++},p_{+-},p_{-+},p_{--})",
      "substitutions": [
        {
          "value": 150.0,
          "unit": "kPa",
          "symbol": "p_corner_pp"
        },
        {
          "value": 150.0,
          "unit": "kPa",
          "symbol": "p_corner_pm"
        },
        {
          "value": 90.0,
          "unit": "kPa",
          "symbol": "p_corner_mp"
        },
        {
          "value": 90.0,
          "unit": "kPa",
          "symbol": "p_corner_mm"
        }
      ],
      "result": {
        "value": 150.0,
        "unit": "kPa"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08."
      }
    },
    {
      "step_id": "edge_limit_multiplier",
      "expression": "edge_limit_multiplier",
      "substitutions": [],
      "result": {
        "value": 1.2,
        "unit": "1"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.26",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "table"
    },
    {
      "step_id": "edge_limit",
      "expression": "p_{edge,lim}=\\lambda_e R",
      "substitutions": [
        {
          "value": 1.2,
          "unit": "1",
          "symbol": "edge_limit_multiplier"
        },
        {
          "value": 152.02,
          "unit": "kPa",
          "symbol": "R"
        }
      ],
      "result": {
        "value": 182.424,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.26",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "step_id": "corner_limit_multiplier",
      "expression": "corner_limit_multiplier",
      "substitutions": [],
      "result": {
        "value": 1.5,
        "unit": "1"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.26",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "table"
    },
    {
      "step_id": "corner_limit",
      "expression": "p_{corner,lim}=\\lambda_c R",
      "substitutions": [
        {
          "value": 1.5,
          "unit": "1",
          "symbol": "corner_limit_multiplier"
        },
        {
          "value": 152.02,
          "unit": "kPa",
          "symbol": "R"
        }
      ],
      "result": {
        "value": 228.03000000000003,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.26",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "step_id": "p_le_R",
      "expression": "p \\le R",
      "substitutions": [
        {
          "value": 120.0,
          "unit": "kPa",
          "symbol": "p"
        },
        {
          "value": 152.02,
          "unit": "kPa",
          "symbol": "R"
        }
      ],
      "result": {
        "value": 120.0,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.7",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "check",
      "operator": "le",
      "right": {
        "value": 152.02,
        "unit": "kPa"
      },
      "passed": true
    },
    {
      "step_id": "p_x_max_le_limit",
      "expression": "p_x_max \\le edge_limit",
      "substitutions": [
        {
          "value": 150.0,
          "unit": "kPa",
          "symbol": "p_x_max"
        },
        {
          "value": 182.424,
          "unit": "kPa",
          "symbol": "edge_limit"
        }
      ],
      "result": {
        "value": 150.0,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.26",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "check",
      "operator": "le",
      "right": {
        "value": 182.424,
        "unit": "kPa"
      },
      "passed": true
    },
    {
      "step_id": "p_y_max_le_limit",
      "expression": "p_y_max \\le edge_limit",
      "substitutions": [
        {
          "value": 120.0,
          "unit": "kPa",
          "symbol": "p_y_max"
        },
        {
          "value": 182.424,
          "unit": "kPa",
          "symbol": "edge_limit"
        }
      ],
      "result": {
        "value": 120.0,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.26",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "check",
      "operator": "le",
      "right": {
        "value": 182.424,
        "unit": "kPa"
      },
      "passed": true
    },
    {
      "step_id": "p_corner_max_le_limit",
      "expression": "p_corner_max \\le corner_limit",
      "substitutions": [
        {
          "value": 150.0,
          "unit": "kPa",
          "symbol": "p_corner_max"
        },
        {
          "value": 228.03000000000003,
          "unit": "kPa",
          "symbol": "corner_limit"
        }
      ],
      "result": {
        "value": 150.0,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.26",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "check",
      "operator": "le",
      "right": {
        "value": 228.03000000000003,
        "unit": "kPa"
      },
      "passed": true
    }
  ],
  "unverified_step_count": 30,
  "result_id": "66666666-6666-4666-8666-666666666666",
  "parameter_source": {
    "kind": "interim",
    "data_sha256": "faaa0724af57ca6c8066f558c4e75c2785d099b34cbfb07c4a85892fdc3b68fe", // pragma: allowlist secret
    "profile": "strict"
  }
} satisfies ResultEnvelope

export const loadsOneAxisJson = "{\"engine_version\":\"0.1.0\",\"input_hash\":\"598e8b96843dbd2bf854325e7e09b3d16e85b58e54d9057402f6fb2e6932a1c0\",\"outputs\":[{\"value\":152.02,\"unit\":\"kPa\",\"quantity\":\"R\",\"rounding_rule\":{\"decimals\":2,\"mode\":\"half_up\"},\"rounding_source\":{\"engineer\":\"Аким\",\"rationale\":\"Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются.\"}},{\"value\":120.0,\"unit\":\"kPa\",\"quantity\":\"p\",\"rounding_rule\":{\"decimals\":2,\"mode\":\"half_up\"},\"rounding_source\":{\"engineer\":\"Аким\",\"rationale\":\"Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются.\"}},{\"value\":90.0,\"unit\":\"kPa\",\"quantity\":\"p_x_min\",\"rounding_rule\":{\"decimals\":2,\"mode\":\"half_up\"},\"rounding_source\":{\"engineer\":\"Аким\",\"rationale\":\"Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются.\"}},{\"value\":150.0,\"unit\":\"kPa\",\"quantity\":\"p_x_max\",\"rounding_rule\":{\"decimals\":2,\"mode\":\"half_up\"},\"rounding_source\":{\"engineer\":\"Аким\",\"rationale\":\"Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются.\"}},{\"value\":120.0,\"unit\":\"kPa\",\"quantity\":\"p_y_min\",\"rounding_rule\":{\"decimals\":2,\"mode\":\"half_up\"},\"rounding_source\":{\"engineer\":\"Аким\",\"rationale\":\"Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются.\"}},{\"value\":120.0,\"unit\":\"kPa\",\"quantity\":\"p_y_max\",\"rounding_rule\":{\"decimals\":2,\"mode\":\"half_up\"},\"rounding_source\":{\"engineer\":\"Аким\",\"rationale\":\"Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются.\"}},{\"value\":150.0,\"unit\":\"kPa\",\"quantity\":\"p_corner_pp\",\"rounding_rule\":{\"decimals\":2,\"mode\":\"half_up\"},\"rounding_source\":{\"engineer\":\"Аким\",\"rationale\":\"Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются.\"}},{\"value\":150.0,\"unit\":\"kPa\",\"quantity\":\"p_corner_pm\",\"rounding_rule\":{\"decimals\":2,\"mode\":\"half_up\"},\"rounding_source\":{\"engineer\":\"Аким\",\"rationale\":\"Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются.\"}},{\"value\":90.0,\"unit\":\"kPa\",\"quantity\":\"p_corner_mp\",\"rounding_rule\":{\"decimals\":2,\"mode\":\"half_up\"},\"rounding_source\":{\"engineer\":\"Аким\",\"rationale\":\"Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются.\"}},{\"value\":90.0,\"unit\":\"kPa\",\"quantity\":\"p_corner_mm\",\"rounding_rule\":{\"decimals\":2,\"mode\":\"half_up\"},\"rounding_source\":{\"engineer\":\"Аким\",\"rationale\":\"Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются.\"}}],\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7, таблица 5.4\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"},{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7, экспликация k\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"},{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7, таблица 5.5\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"},{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7, экспликация k_z\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"},{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7, формула (5.7)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"},{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.28, explanation of formula (5.11)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"},{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.28, formula (5.11)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"},{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.28, applicability of formula (5.11)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"},{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.27, figure 5.1\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"},{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.29, formula (5.15)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"},{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.26\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"},{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"engineer_rules\":[{\"engineer\":\"Аким\",\"rationale\":\"Геометрия прямоугольной подошвы: A=b*l, Wx=l*b²/6, Wy=b*l²/6; инженерный контракт 2026-11-08.\"},{\"engineer\":\"Аким\",\"rationale\":\"Подписанный перенос нагрузок к подошве M_base=M+Q*h; оси x=b и y=l; инженерный контракт 2026-11-08.\"},{\"engineer\":\"Аким\",\"rationale\":\"Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08.\"},{\"engineer\":\"Аким\",\"rationale\":\"Полный контакт прямоугольной подошвы: минимум четырёх подписанных угловых давлений неотрицателен; решение инженера 2026-11-08.\"},{\"engineer\":\"Аким\",\"rationale\":\"Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются.\"}],\"verdict\":\"pass\",\"verdict_reason\":{\"kind\":\"check\",\"step_id\":\"p_corner_max_le_limit\"},\"warnings\":[],\"trace\":[{\"step_id\":\"gamma_c1\",\"expression\":\"\\\\gamma_{c1}\",\"substitutions\":[],\"result\":{\"value\":1.1,\"unit\":\"1\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7, таблица 5.4\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"table\"},{\"step_id\":\"gamma_c2\",\"expression\":\"\\\\gamma_{c2}\",\"substitutions\":[],\"result\":{\"value\":1.0,\"unit\":\"1\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7, таблица 5.4\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"table\"},{\"step_id\":\"k\",\"expression\":\"k\",\"substitutions\":[],\"result\":{\"value\":1.0,\"unit\":\"1\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7, экспликация k\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"table\"},{\"step_id\":\"M_gamma\",\"expression\":\"M_{\\\\gamma} = M_{\\\\gamma}\\\\left(\\\\varphi_{II}\\\\right)\",\"substitutions\":[{\"value\":20.0,\"unit\":\"deg\",\"symbol\":\"phi_II\"}],\"result\":{\"value\":0.51,\"unit\":\"1\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7, таблица 5.5\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"table\"},{\"step_id\":\"M_q\",\"expression\":\"M_{q} = M_{q}\\\\left(\\\\varphi_{II}\\\\right)\",\"substitutions\":[{\"value\":20.0,\"unit\":\"deg\",\"symbol\":\"phi_II\"}],\"result\":{\"value\":3.06,\"unit\":\"1\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7, таблица 5.5\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"table\"},{\"step_id\":\"M_c\",\"expression\":\"M_{c} = M_{c}\\\\left(\\\\varphi_{II}\\\\right)\",\"substitutions\":[{\"value\":20.0,\"unit\":\"deg\",\"symbol\":\"phi_II\"}],\"result\":{\"value\":5.66,\"unit\":\"1\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7, таблица 5.5\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"table\"},{\"step_id\":\"k_z\",\"expression\":\"k_{z}=1\",\"substitutions\":[],\"result\":{\"value\":1.0,\"unit\":\"1\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7, экспликация k_z\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"step_id\":\"R\",\"expression\":\"R=\\\\frac{\\\\gamma_{c1}\\\\gamma_{c2}}{k}\\\\left[M_{\\\\gamma}k_{z}b\\\\gamma_{II}+M_{q}d_{1}\\\\gamma'_{II}+(M_{q}-1)d_{b}\\\\gamma'_{II}+M_{c}c_{II}\\\\right]\",\"substitutions\":[{\"value\":1.1,\"unit\":\"1\",\"symbol\":\"gamma_c1\"},{\"value\":1.0,\"unit\":\"1\",\"symbol\":\"gamma_c2\"},{\"value\":1.0,\"unit\":\"1\",\"symbol\":\"k\"},{\"value\":0.51,\"unit\":\"1\",\"symbol\":\"M_gamma\"},{\"value\":1.0,\"unit\":\"1\",\"symbol\":\"k_z\"},{\"value\":2.0,\"unit\":\"m\",\"symbol\":\"b\"},{\"value\":20.0,\"unit\":\"kN/m3\",\"symbol\":\"gamma_II\"},{\"value\":3.06,\"unit\":\"1\",\"symbol\":\"M_q\"},{\"value\":1.0,\"unit\":\"m\",\"symbol\":\"d_1\"},{\"value\":20.0,\"unit\":\"kN/m3\",\"symbol\":\"gamma_II_prime\"},{\"value\":0.0,\"unit\":\"m\",\"symbol\":\"d_b\"},{\"value\":5.66,\"unit\":\"1\",\"symbol\":\"M_c\"},{\"value\":10.0,\"unit\":\"kPa\",\"symbol\":\"c_II\"}],\"result\":{\"value\":152.02,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7, формула (5.7)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"kind\":\"engineer_formula\",\"step_id\":\"A\",\"expression\":\"A=b l\",\"substitutions\":[{\"value\":2.0,\"unit\":\"m\",\"symbol\":\"b\"},{\"value\":3.0,\"unit\":\"m\",\"symbol\":\"l\"}],\"result\":{\"value\":6.0,\"unit\":\"m2\"},\"source\":{\"engineer\":\"Аким\",\"rationale\":\"Геометрия прямоугольной подошвы: A=b*l, Wx=l*b²/6, Wy=b*l²/6; инженерный контракт 2026-11-08.\"}},{\"kind\":\"engineer_formula\",\"step_id\":\"Wx\",\"expression\":\"W_x=l b^2/6\",\"substitutions\":[{\"value\":2.0,\"unit\":\"m\",\"symbol\":\"b\"},{\"value\":3.0,\"unit\":\"m\",\"symbol\":\"l\"}],\"result\":{\"value\":2.0,\"unit\":\"m3\"},\"source\":{\"engineer\":\"Аким\",\"rationale\":\"Геометрия прямоугольной подошвы: A=b*l, Wx=l*b²/6, Wy=b*l²/6; инженерный контракт 2026-11-08.\"}},{\"kind\":\"engineer_formula\",\"step_id\":\"Wy\",\"expression\":\"W_y=b l^2/6\",\"substitutions\":[{\"value\":2.0,\"unit\":\"m\",\"symbol\":\"b\"},{\"value\":3.0,\"unit\":\"m\",\"symbol\":\"l\"}],\"result\":{\"value\":3.0,\"unit\":\"m3\"},\"source\":{\"engineer\":\"Аким\",\"rationale\":\"Геометрия прямоугольной подошвы: A=b*l, Wx=l*b²/6, Wy=b*l²/6; инженерный контракт 2026-11-08.\"}},{\"kind\":\"engineer_formula\",\"step_id\":\"Mx_base\",\"expression\":\"M_{x,base}=M_x+Q_x h\",\"substitutions\":[{\"value\":40.0,\"unit\":\"kN*m\",\"symbol\":\"Mx\"},{\"value\":20.0,\"unit\":\"kN\",\"symbol\":\"Qx\"},{\"value\":1.0,\"unit\":\"m\",\"symbol\":\"h\"}],\"result\":{\"value\":60.0,\"unit\":\"kN*m\"},\"source\":{\"engineer\":\"Аким\",\"rationale\":\"Подписанный перенос нагрузок к подошве M_base=M+Q*h; оси x=b и y=l; инженерный контракт 2026-11-08.\"}},{\"kind\":\"engineer_formula\",\"step_id\":\"My_base\",\"expression\":\"M_{y,base}=M_y+Q_y h\",\"substitutions\":[{\"value\":0.0,\"unit\":\"kN*m\",\"symbol\":\"My\"},{\"value\":0.0,\"unit\":\"kN\",\"symbol\":\"Qy\"},{\"value\":1.0,\"unit\":\"m\",\"symbol\":\"h\"}],\"result\":{\"value\":0.0,\"unit\":\"kN*m\"},\"source\":{\"engineer\":\"Аким\",\"rationale\":\"Подписанный перенос нагрузок к подошве M_base=M+Q*h; оси x=b и y=l; инженерный контракт 2026-11-08.\"}},{\"step_id\":\"gamma_mt\",\"expression\":\"\\\\gamma_{mt}\",\"substitutions\":[],\"result\":{\"value\":20.0,\"unit\":\"kN/m3\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.28, explanation of formula (5.11)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"table\"},{\"step_id\":\"p\",\"expression\":\"p_{+}=\\\\frac{N}{A}+\\\\gamma_{mt}d+\\\\frac{M}{W}\",\"substitutions\":[{\"value\":600.0,\"unit\":\"kN\",\"symbol\":\"N\"},{\"value\":6.0,\"unit\":\"m2\",\"symbol\":\"A\"},{\"value\":20.0,\"unit\":\"kN/m3\",\"symbol\":\"gamma_mt\"},{\"value\":1.0,\"unit\":\"m\",\"symbol\":\"d\"},{\"value\":0.0,\"unit\":\"kN*m\",\"symbol\":\"M\"},{\"value\":2.0,\"unit\":\"m3\",\"symbol\":\"W\"}],\"result\":{\"value\":120.0,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.28, formula (5.11)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"kind\":\"engineer_formula\",\"step_id\":\"V\",\"expression\":\"V=N+\\\\gamma_{mt} d A\",\"substitutions\":[{\"value\":600.0,\"unit\":\"kN\",\"symbol\":\"N\"},{\"value\":20.0,\"unit\":\"kN/m3\",\"symbol\":\"gamma_mt\"},{\"value\":1.0,\"unit\":\"m\",\"symbol\":\"d\"},{\"value\":6.0,\"unit\":\"m2\",\"symbol\":\"A\"}],\"result\":{\"value\":720.0,\"unit\":\"kN\"},\"source\":{\"engineer\":\"Аким\",\"rationale\":\"Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08.\"}},{\"step_id\":\"p_x_min\",\"expression\":\"p_{-}=\\\\frac{N}{A}+\\\\gamma_{mt}d-\\\\frac{M}{W}\",\"substitutions\":[{\"value\":600.0,\"unit\":\"kN\",\"symbol\":\"N\"},{\"value\":6.0,\"unit\":\"m2\",\"symbol\":\"A\"},{\"value\":20.0,\"unit\":\"kN/m3\",\"symbol\":\"gamma_mt\"},{\"value\":1.0,\"unit\":\"m\",\"symbol\":\"d\"},{\"value\":60.0,\"unit\":\"kN*m\",\"symbol\":\"M\"},{\"value\":2.0,\"unit\":\"m3\",\"symbol\":\"W\"}],\"result\":{\"value\":90.0,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.28, formula (5.11)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"step_id\":\"p_x_max\",\"expression\":\"p_{+}=\\\\frac{N}{A}+\\\\gamma_{mt}d+\\\\frac{M}{W}\",\"substitutions\":[{\"value\":600.0,\"unit\":\"kN\",\"symbol\":\"N\"},{\"value\":6.0,\"unit\":\"m2\",\"symbol\":\"A\"},{\"value\":20.0,\"unit\":\"kN/m3\",\"symbol\":\"gamma_mt\"},{\"value\":1.0,\"unit\":\"m\",\"symbol\":\"d\"},{\"value\":60.0,\"unit\":\"kN*m\",\"symbol\":\"M\"},{\"value\":2.0,\"unit\":\"m3\",\"symbol\":\"W\"}],\"result\":{\"value\":150.0,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.28, formula (5.11)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"kind\":\"engineer_formula\",\"step_id\":\"e_x\",\"expression\":\"e_x=|M_{x,base}|/V\",\"substitutions\":[{\"value\":60.0,\"unit\":\"kN*m\",\"symbol\":\"Mx_base\"},{\"value\":720.0,\"unit\":\"kN\",\"symbol\":\"V\"}],\"result\":{\"value\":0.08333333333333333,\"unit\":\"m\"},\"source\":{\"engineer\":\"Аким\",\"rationale\":\"Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08.\"}},{\"step_id\":\"relative_eccentricity_x\",\"expression\":\"e/l\\\\leq1/6\",\"substitutions\":[{\"value\":0.041666666666666664,\"unit\":\"1\",\"symbol\":\"e/L\"},{\"value\":1.0,\"unit\":\"1\",\"symbol\":\"numerator\"},{\"value\":6.0,\"unit\":\"1\",\"symbol\":\"denominator\"}],\"result\":{\"value\":1.0,\"unit\":\"1\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.28, applicability of formula (5.11)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"step_id\":\"pressure_diagram_x\",\"expression\":\"e<l/6\",\"substitutions\":[{\"value\":0.08333333333333333,\"unit\":\"m\",\"symbol\":\"e\"},{\"value\":2.0,\"unit\":\"m\",\"symbol\":\"l\"}],\"result\":{\"value\":0.08333333333333333,\"unit\":\"m\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.27, figure 5.1\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"step_id\":\"p_y_min\",\"expression\":\"p_{-}=\\\\frac{N}{A}+\\\\gamma_{mt}d-\\\\frac{M}{W}\",\"substitutions\":[{\"value\":600.0,\"unit\":\"kN\",\"symbol\":\"N\"},{\"value\":6.0,\"unit\":\"m2\",\"symbol\":\"A\"},{\"value\":20.0,\"unit\":\"kN/m3\",\"symbol\":\"gamma_mt\"},{\"value\":1.0,\"unit\":\"m\",\"symbol\":\"d\"},{\"value\":0.0,\"unit\":\"kN*m\",\"symbol\":\"M\"},{\"value\":3.0,\"unit\":\"m3\",\"symbol\":\"W\"}],\"result\":{\"value\":120.0,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.28, formula (5.11)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"step_id\":\"p_y_max\",\"expression\":\"p_{+}=\\\\frac{N}{A}+\\\\gamma_{mt}d+\\\\frac{M}{W}\",\"substitutions\":[{\"value\":600.0,\"unit\":\"kN\",\"symbol\":\"N\"},{\"value\":6.0,\"unit\":\"m2\",\"symbol\":\"A\"},{\"value\":20.0,\"unit\":\"kN/m3\",\"symbol\":\"gamma_mt\"},{\"value\":1.0,\"unit\":\"m\",\"symbol\":\"d\"},{\"value\":0.0,\"unit\":\"kN*m\",\"symbol\":\"M\"},{\"value\":3.0,\"unit\":\"m3\",\"symbol\":\"W\"}],\"result\":{\"value\":120.0,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.28, formula (5.11)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"kind\":\"engineer_formula\",\"step_id\":\"e_y\",\"expression\":\"e_y=|M_{y,base}|/V\",\"substitutions\":[{\"value\":0.0,\"unit\":\"kN*m\",\"symbol\":\"My_base\"},{\"value\":720.0,\"unit\":\"kN\",\"symbol\":\"V\"}],\"result\":{\"value\":0.0,\"unit\":\"m\"},\"source\":{\"engineer\":\"Аким\",\"rationale\":\"Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08.\"}},{\"step_id\":\"relative_eccentricity_y\",\"expression\":\"e/l\\\\leq1/6\",\"substitutions\":[{\"value\":0.0,\"unit\":\"1\",\"symbol\":\"e/L\"},{\"value\":1.0,\"unit\":\"1\",\"symbol\":\"numerator\"},{\"value\":6.0,\"unit\":\"1\",\"symbol\":\"denominator\"}],\"result\":{\"value\":1.0,\"unit\":\"1\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.28, applicability of formula (5.11)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"step_id\":\"pressure_diagram_y\",\"expression\":\"e<l/6\",\"substitutions\":[{\"value\":0.0,\"unit\":\"m\",\"symbol\":\"e\"},{\"value\":3.0,\"unit\":\"m\",\"symbol\":\"l\"}],\"result\":{\"value\":0.0,\"unit\":\"m\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.27, figure 5.1\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"step_id\":\"corner_component_pp\",\"expression\":\"P_{\\\\max}=\\\\frac{N}{A}+\\\\gamma_{mt}d+\\\\frac{M_x}{W_x}+\\\\frac{M_y}{W_y}\",\"substitutions\":[{\"value\":600.0,\"unit\":\"kN\",\"symbol\":\"N\"},{\"value\":6.0,\"unit\":\"m2\",\"symbol\":\"A\"},{\"value\":20.0,\"unit\":\"kN/m3\",\"symbol\":\"gamma_mt\"},{\"value\":1.0,\"unit\":\"m\",\"symbol\":\"d\"},{\"value\":60.0,\"unit\":\"kN*m\",\"symbol\":\"M_x\"},{\"value\":2.0,\"unit\":\"m3\",\"symbol\":\"W_x\"},{\"value\":0.0,\"unit\":\"kN*m\",\"symbol\":\"M_y\"},{\"value\":3.0,\"unit\":\"m3\",\"symbol\":\"W_y\"}],\"result\":{\"value\":150.0,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.29, formula (5.15)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"kind\":\"engineer_formula\",\"step_id\":\"p_corner_pp\",\"expression\":\"p_{pp}=p+s_x M_{x,base}/W_x+s_y M_{y,base}/W_y\",\"substitutions\":[{\"value\":120.0,\"unit\":\"kPa\",\"symbol\":\"p\"},{\"value\":60.0,\"unit\":\"kN*m\",\"symbol\":\"Mx_base\"},{\"value\":2.0,\"unit\":\"m3\",\"symbol\":\"Wx\"},{\"value\":0.0,\"unit\":\"kN*m\",\"symbol\":\"My_base\"},{\"value\":3.0,\"unit\":\"m3\",\"symbol\":\"Wy\"},{\"value\":1.0,\"unit\":\"1\",\"symbol\":\"sign_x_pp\"},{\"value\":1.0,\"unit\":\"1\",\"symbol\":\"sign_y_pp\"},{\"value\":150.0,\"unit\":\"kPa\",\"symbol\":\"corner_component_pp\"}],\"result\":{\"value\":150.0,\"unit\":\"kPa\"},\"source\":{\"engineer\":\"Аким\",\"rationale\":\"Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08.\"}},{\"step_id\":\"corner_component_pm\",\"expression\":\"P_{\\\\max}=\\\\frac{N}{A}+\\\\gamma_{mt}d+\\\\frac{M_x}{W_x}+\\\\frac{M_y}{W_y}\",\"substitutions\":[{\"value\":600.0,\"unit\":\"kN\",\"symbol\":\"N\"},{\"value\":6.0,\"unit\":\"m2\",\"symbol\":\"A\"},{\"value\":20.0,\"unit\":\"kN/m3\",\"symbol\":\"gamma_mt\"},{\"value\":1.0,\"unit\":\"m\",\"symbol\":\"d\"},{\"value\":60.0,\"unit\":\"kN*m\",\"symbol\":\"M_x\"},{\"value\":2.0,\"unit\":\"m3\",\"symbol\":\"W_x\"},{\"value\":-0.0,\"unit\":\"kN*m\",\"symbol\":\"M_y\"},{\"value\":3.0,\"unit\":\"m3\",\"symbol\":\"W_y\"}],\"result\":{\"value\":150.0,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.29, formula (5.15)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"kind\":\"engineer_formula\",\"step_id\":\"p_corner_pm\",\"expression\":\"p_{pm}=p+s_x M_{x,base}/W_x+s_y M_{y,base}/W_y\",\"substitutions\":[{\"value\":120.0,\"unit\":\"kPa\",\"symbol\":\"p\"},{\"value\":60.0,\"unit\":\"kN*m\",\"symbol\":\"Mx_base\"},{\"value\":2.0,\"unit\":\"m3\",\"symbol\":\"Wx\"},{\"value\":0.0,\"unit\":\"kN*m\",\"symbol\":\"My_base\"},{\"value\":3.0,\"unit\":\"m3\",\"symbol\":\"Wy\"},{\"value\":1.0,\"unit\":\"1\",\"symbol\":\"sign_x_pm\"},{\"value\":-1.0,\"unit\":\"1\",\"symbol\":\"sign_y_pm\"},{\"value\":150.0,\"unit\":\"kPa\",\"symbol\":\"corner_component_pm\"}],\"result\":{\"value\":150.0,\"unit\":\"kPa\"},\"source\":{\"engineer\":\"Аким\",\"rationale\":\"Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08.\"}},{\"step_id\":\"corner_component_mp\",\"expression\":\"P_{\\\\max}=\\\\frac{N}{A}+\\\\gamma_{mt}d+\\\\frac{M_x}{W_x}+\\\\frac{M_y}{W_y}\",\"substitutions\":[{\"value\":600.0,\"unit\":\"kN\",\"symbol\":\"N\"},{\"value\":6.0,\"unit\":\"m2\",\"symbol\":\"A\"},{\"value\":20.0,\"unit\":\"kN/m3\",\"symbol\":\"gamma_mt\"},{\"value\":1.0,\"unit\":\"m\",\"symbol\":\"d\"},{\"value\":-60.0,\"unit\":\"kN*m\",\"symbol\":\"M_x\"},{\"value\":2.0,\"unit\":\"m3\",\"symbol\":\"W_x\"},{\"value\":0.0,\"unit\":\"kN*m\",\"symbol\":\"M_y\"},{\"value\":3.0,\"unit\":\"m3\",\"symbol\":\"W_y\"}],\"result\":{\"value\":90.0,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.29, formula (5.15)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"kind\":\"engineer_formula\",\"step_id\":\"p_corner_mp\",\"expression\":\"p_{mp}=p+s_x M_{x,base}/W_x+s_y M_{y,base}/W_y\",\"substitutions\":[{\"value\":120.0,\"unit\":\"kPa\",\"symbol\":\"p\"},{\"value\":60.0,\"unit\":\"kN*m\",\"symbol\":\"Mx_base\"},{\"value\":2.0,\"unit\":\"m3\",\"symbol\":\"Wx\"},{\"value\":0.0,\"unit\":\"kN*m\",\"symbol\":\"My_base\"},{\"value\":3.0,\"unit\":\"m3\",\"symbol\":\"Wy\"},{\"value\":-1.0,\"unit\":\"1\",\"symbol\":\"sign_x_mp\"},{\"value\":1.0,\"unit\":\"1\",\"symbol\":\"sign_y_mp\"},{\"value\":90.0,\"unit\":\"kPa\",\"symbol\":\"corner_component_mp\"}],\"result\":{\"value\":90.0,\"unit\":\"kPa\"},\"source\":{\"engineer\":\"Аким\",\"rationale\":\"Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08.\"}},{\"step_id\":\"corner_component_mm\",\"expression\":\"P_{\\\\max}=\\\\frac{N}{A}+\\\\gamma_{mt}d+\\\\frac{M_x}{W_x}+\\\\frac{M_y}{W_y}\",\"substitutions\":[{\"value\":600.0,\"unit\":\"kN\",\"symbol\":\"N\"},{\"value\":6.0,\"unit\":\"m2\",\"symbol\":\"A\"},{\"value\":20.0,\"unit\":\"kN/m3\",\"symbol\":\"gamma_mt\"},{\"value\":1.0,\"unit\":\"m\",\"symbol\":\"d\"},{\"value\":-60.0,\"unit\":\"kN*m\",\"symbol\":\"M_x\"},{\"value\":2.0,\"unit\":\"m3\",\"symbol\":\"W_x\"},{\"value\":-0.0,\"unit\":\"kN*m\",\"symbol\":\"M_y\"},{\"value\":3.0,\"unit\":\"m3\",\"symbol\":\"W_y\"}],\"result\":{\"value\":90.0,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.29, formula (5.15)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"kind\":\"engineer_formula\",\"step_id\":\"p_corner_mm\",\"expression\":\"p_{mm}=p+s_x M_{x,base}/W_x+s_y M_{y,base}/W_y\",\"substitutions\":[{\"value\":120.0,\"unit\":\"kPa\",\"symbol\":\"p\"},{\"value\":60.0,\"unit\":\"kN*m\",\"symbol\":\"Mx_base\"},{\"value\":2.0,\"unit\":\"m3\",\"symbol\":\"Wx\"},{\"value\":0.0,\"unit\":\"kN*m\",\"symbol\":\"My_base\"},{\"value\":3.0,\"unit\":\"m3\",\"symbol\":\"Wy\"},{\"value\":-1.0,\"unit\":\"1\",\"symbol\":\"sign_x_mm\"},{\"value\":-1.0,\"unit\":\"1\",\"symbol\":\"sign_y_mm\"},{\"value\":90.0,\"unit\":\"kPa\",\"symbol\":\"corner_component_mm\"}],\"result\":{\"value\":90.0,\"unit\":\"kPa\"},\"source\":{\"engineer\":\"Аким\",\"rationale\":\"Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08.\"}},{\"kind\":\"engineer_formula\",\"step_id\":\"p_corner_min\",\"expression\":\"p_{corner,min}=\\\\min(p_{++},p_{+-},p_{-+},p_{--})\",\"substitutions\":[{\"value\":150.0,\"unit\":\"kPa\",\"symbol\":\"p_corner_pp\"},{\"value\":150.0,\"unit\":\"kPa\",\"symbol\":\"p_corner_pm\"},{\"value\":90.0,\"unit\":\"kPa\",\"symbol\":\"p_corner_mp\"},{\"value\":90.0,\"unit\":\"kPa\",\"symbol\":\"p_corner_mm\"}],\"result\":{\"value\":90.0,\"unit\":\"kPa\"},\"source\":{\"engineer\":\"Аким\",\"rationale\":\"Полный контакт прямоугольной подошвы: минимум четырёх подписанных угловых давлений неотрицателен; решение инженера 2026-11-08.\"}},{\"kind\":\"engineer_formula\",\"step_id\":\"p_corner_max\",\"expression\":\"p_{corner,max}=\\\\max(p_{++},p_{+-},p_{-+},p_{--})\",\"substitutions\":[{\"value\":150.0,\"unit\":\"kPa\",\"symbol\":\"p_corner_pp\"},{\"value\":150.0,\"unit\":\"kPa\",\"symbol\":\"p_corner_pm\"},{\"value\":90.0,\"unit\":\"kPa\",\"symbol\":\"p_corner_mp\"},{\"value\":90.0,\"unit\":\"kPa\",\"symbol\":\"p_corner_mm\"}],\"result\":{\"value\":150.0,\"unit\":\"kPa\"},\"source\":{\"engineer\":\"Аким\",\"rationale\":\"Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08.\"}},{\"step_id\":\"edge_limit_multiplier\",\"expression\":\"edge_limit_multiplier\",\"substitutions\":[],\"result\":{\"value\":1.2,\"unit\":\"1\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.26\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"table\"},{\"step_id\":\"edge_limit\",\"expression\":\"p_{edge,lim}=\\\\lambda_e R\",\"substitutions\":[{\"value\":1.2,\"unit\":\"1\",\"symbol\":\"edge_limit_multiplier\"},{\"value\":152.02,\"unit\":\"kPa\",\"symbol\":\"R\"}],\"result\":{\"value\":182.424,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.26\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"step_id\":\"corner_limit_multiplier\",\"expression\":\"corner_limit_multiplier\",\"substitutions\":[],\"result\":{\"value\":1.5,\"unit\":\"1\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.26\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"table\"},{\"step_id\":\"corner_limit\",\"expression\":\"p_{corner,lim}=\\\\lambda_c R\",\"substitutions\":[{\"value\":1.5,\"unit\":\"1\",\"symbol\":\"corner_limit_multiplier\"},{\"value\":152.02,\"unit\":\"kPa\",\"symbol\":\"R\"}],\"result\":{\"value\":228.03000000000003,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.26\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"step_id\":\"p_le_R\",\"expression\":\"p \\\\le R\",\"substitutions\":[{\"value\":120.0,\"unit\":\"kPa\",\"symbol\":\"p\"},{\"value\":152.02,\"unit\":\"kPa\",\"symbol\":\"R\"}],\"result\":{\"value\":120.0,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"check\",\"operator\":\"le\",\"right\":{\"value\":152.02,\"unit\":\"kPa\"},\"passed\":true},{\"step_id\":\"p_x_max_le_limit\",\"expression\":\"p_x_max \\\\le edge_limit\",\"substitutions\":[{\"value\":150.0,\"unit\":\"kPa\",\"symbol\":\"p_x_max\"},{\"value\":182.424,\"unit\":\"kPa\",\"symbol\":\"edge_limit\"}],\"result\":{\"value\":150.0,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.26\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"check\",\"operator\":\"le\",\"right\":{\"value\":182.424,\"unit\":\"kPa\"},\"passed\":true},{\"step_id\":\"p_y_max_le_limit\",\"expression\":\"p_y_max \\\\le edge_limit\",\"substitutions\":[{\"value\":120.0,\"unit\":\"kPa\",\"symbol\":\"p_y_max\"},{\"value\":182.424,\"unit\":\"kPa\",\"symbol\":\"edge_limit\"}],\"result\":{\"value\":120.0,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.26\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"check\",\"operator\":\"le\",\"right\":{\"value\":182.424,\"unit\":\"kPa\"},\"passed\":true},{\"step_id\":\"p_corner_max_le_limit\",\"expression\":\"p_corner_max \\\\le corner_limit\",\"substitutions\":[{\"value\":150.0,\"unit\":\"kPa\",\"symbol\":\"p_corner_max\"},{\"value\":228.03000000000003,\"unit\":\"kPa\",\"symbol\":\"corner_limit\"}],\"result\":{\"value\":150.0,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.26\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"check\",\"operator\":\"le\",\"right\":{\"value\":228.03000000000003,\"unit\":\"kPa\"},\"passed\":true}],\"unverified_step_count\":30,\"result_id\":\"66666666-6666-4666-8666-666666666666\",\"parameter_source\":{\"kind\":\"interim\",\"data_sha256\":\"faaa0724af57ca6c8066f558c4e75c2785d099b34cbfb07c4a85892fdc3b68fe\",\"profile\":\"strict\"}}"

export const LOADS_BIAXIAL_ID = '77777777-7777-4777-8777-777777777777'

export const loadsBiaxialInputs = {
  "b": {
    "value": 2,
    "unit": "m"
  },
  "d_1": {
    "value": 1,
    "unit": "m"
  },
  "d_b": {
    "value": 0,
    "unit": "m"
  },
  "gamma_II": {
    "value": 20,
    "unit": "kN/m3"
  },
  "gamma_II_prime": {
    "value": 20,
    "unit": "kN/m3"
  },
  "c_II": {
    "value": 10,
    "unit": "kPa"
  },
  "phi_II": {
    "value": 20,
    "unit": "deg"
  },
  "l": {
    "value": 3,
    "unit": "m"
  },
  "h": {
    "value": 1,
    "unit": "m"
  },
  "d": {
    "value": 1,
    "unit": "m"
  },
  "N": {
    "value": 600,
    "unit": "kN"
  },
  "Mx": {
    "value": 40,
    "unit": "kN*m"
  },
  "My": {
    "value": -30,
    "unit": "kN*m"
  },
  "Qx": {
    "value": 20,
    "unit": "kN"
  },
  "Qy": {
    "value": -15,
    "unit": "kN"
  }
} satisfies CalculationRequest['inputs']

export const loadsBiaxialEnvelope = {
  "engine_version": "0.1.0",
  "input_hash": "75aea1a6c3764d8ed86f3e35f8b54a8aaa352d71e0b8e2b3228d08fa83e0eb6d", // pragma: allowlist secret
  "outputs": [
    {
      "value": 152.02,
      "unit": "kPa",
      "quantity": "R",
      "rounding_rule": {
        "decimals": 2,
        "mode": "half_up"
      },
      "rounding_source": {
        "engineer": "Аким",
        "rationale": "Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются."
      }
    },
    {
      "value": 120.0,
      "unit": "kPa",
      "quantity": "p",
      "rounding_rule": {
        "decimals": 2,
        "mode": "half_up"
      },
      "rounding_source": {
        "engineer": "Аким",
        "rationale": "Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются."
      }
    },
    {
      "value": 90.0,
      "unit": "kPa",
      "quantity": "p_x_min",
      "rounding_rule": {
        "decimals": 2,
        "mode": "half_up"
      },
      "rounding_source": {
        "engineer": "Аким",
        "rationale": "Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются."
      }
    },
    {
      "value": 150.0,
      "unit": "kPa",
      "quantity": "p_x_max",
      "rounding_rule": {
        "decimals": 2,
        "mode": "half_up"
      },
      "rounding_source": {
        "engineer": "Аким",
        "rationale": "Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются."
      }
    },
    {
      "value": 105.0,
      "unit": "kPa",
      "quantity": "p_y_min",
      "rounding_rule": {
        "decimals": 2,
        "mode": "half_up"
      },
      "rounding_source": {
        "engineer": "Аким",
        "rationale": "Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются."
      }
    },
    {
      "value": 135.0,
      "unit": "kPa",
      "quantity": "p_y_max",
      "rounding_rule": {
        "decimals": 2,
        "mode": "half_up"
      },
      "rounding_source": {
        "engineer": "Аким",
        "rationale": "Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются."
      }
    },
    {
      "value": 135.0,
      "unit": "kPa",
      "quantity": "p_corner_pp",
      "rounding_rule": {
        "decimals": 2,
        "mode": "half_up"
      },
      "rounding_source": {
        "engineer": "Аким",
        "rationale": "Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются."
      }
    },
    {
      "value": 165.0,
      "unit": "kPa",
      "quantity": "p_corner_pm",
      "rounding_rule": {
        "decimals": 2,
        "mode": "half_up"
      },
      "rounding_source": {
        "engineer": "Аким",
        "rationale": "Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются."
      }
    },
    {
      "value": 75.0,
      "unit": "kPa",
      "quantity": "p_corner_mp",
      "rounding_rule": {
        "decimals": 2,
        "mode": "half_up"
      },
      "rounding_source": {
        "engineer": "Аким",
        "rationale": "Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются."
      }
    },
    {
      "value": 105.0,
      "unit": "kPa",
      "quantity": "p_corner_mm",
      "rounding_rule": {
        "decimals": 2,
        "mode": "half_up"
      },
      "rounding_source": {
        "engineer": "Аким",
        "rationale": "Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются."
      }
    }
  ],
  "norm_refs": [
    {
      "document": "СП 22.13330.2016",
      "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
      "clause": "5.6.7, таблица 5.4",
      "status": "unverified",
      "provenance": "machine-extracted"
    },
    {
      "document": "СП 22.13330.2016",
      "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
      "clause": "5.6.7, экспликация k",
      "status": "unverified",
      "provenance": "machine-extracted"
    },
    {
      "document": "СП 22.13330.2016",
      "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
      "clause": "5.6.7, таблица 5.5",
      "status": "unverified",
      "provenance": "machine-extracted"
    },
    {
      "document": "СП 22.13330.2016",
      "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
      "clause": "5.6.7, экспликация k_z",
      "status": "unverified",
      "provenance": "machine-extracted"
    },
    {
      "document": "СП 22.13330.2016",
      "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
      "clause": "5.6.7, формула (5.7)",
      "status": "unverified",
      "provenance": "machine-extracted"
    },
    {
      "document": "СП 22.13330.2016",
      "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
      "clause": "5.6.28, explanation of formula (5.11)",
      "status": "unverified",
      "provenance": "machine-extracted"
    },
    {
      "document": "СП 22.13330.2016",
      "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
      "clause": "5.6.28, formula (5.11)",
      "status": "unverified",
      "provenance": "machine-extracted"
    },
    {
      "document": "СП 22.13330.2016",
      "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
      "clause": "5.6.28, applicability of formula (5.11)",
      "status": "unverified",
      "provenance": "machine-extracted"
    },
    {
      "document": "СП 22.13330.2016",
      "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
      "clause": "5.6.27, figure 5.1",
      "status": "unverified",
      "provenance": "machine-extracted"
    },
    {
      "document": "СП 22.13330.2016",
      "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
      "clause": "5.6.29, formula (5.15)",
      "status": "unverified",
      "provenance": "machine-extracted"
    },
    {
      "document": "СП 22.13330.2016",
      "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
      "clause": "5.6.26",
      "status": "unverified",
      "provenance": "machine-extracted"
    },
    {
      "document": "СП 22.13330.2016",
      "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
      "clause": "5.6.7",
      "status": "unverified",
      "provenance": "machine-extracted"
    }
  ],
  "engineer_rules": [
    {
      "engineer": "Аким",
      "rationale": "Геометрия прямоугольной подошвы: A=b*l, Wx=l*b²/6, Wy=b*l²/6; инженерный контракт 2026-11-08."
    },
    {
      "engineer": "Аким",
      "rationale": "Подписанный перенос нагрузок к подошве M_base=M+Q*h; оси x=b и y=l; инженерный контракт 2026-11-08."
    },
    {
      "engineer": "Аким",
      "rationale": "Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08."
    },
    {
      "engineer": "Аким",
      "rationale": "Полный контакт прямоугольной подошвы: минимум четырёх подписанных угловых давлений неотрицателен; решение инженера 2026-11-08."
    },
    {
      "engineer": "Аким",
      "rationale": "Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются."
    }
  ],
  "verdict": "pass",
  "verdict_reason": {
    "kind": "check",
    "step_id": "p_corner_max_le_limit"
  },
  "warnings": [],
  "trace": [
    {
      "step_id": "gamma_c1",
      "expression": "\\gamma_{c1}",
      "substitutions": [],
      "result": {
        "value": 1.1,
        "unit": "1"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.7, таблица 5.4",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "table"
    },
    {
      "step_id": "gamma_c2",
      "expression": "\\gamma_{c2}",
      "substitutions": [],
      "result": {
        "value": 1.0,
        "unit": "1"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.7, таблица 5.4",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "table"
    },
    {
      "step_id": "k",
      "expression": "k",
      "substitutions": [],
      "result": {
        "value": 1.0,
        "unit": "1"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.7, экспликация k",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "table"
    },
    {
      "step_id": "M_gamma",
      "expression": "M_{\\gamma} = M_{\\gamma}\\left(\\varphi_{II}\\right)",
      "substitutions": [
        {
          "value": 20.0,
          "unit": "deg",
          "symbol": "phi_II"
        }
      ],
      "result": {
        "value": 0.51,
        "unit": "1"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.7, таблица 5.5",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "table"
    },
    {
      "step_id": "M_q",
      "expression": "M_{q} = M_{q}\\left(\\varphi_{II}\\right)",
      "substitutions": [
        {
          "value": 20.0,
          "unit": "deg",
          "symbol": "phi_II"
        }
      ],
      "result": {
        "value": 3.06,
        "unit": "1"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.7, таблица 5.5",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "table"
    },
    {
      "step_id": "M_c",
      "expression": "M_{c} = M_{c}\\left(\\varphi_{II}\\right)",
      "substitutions": [
        {
          "value": 20.0,
          "unit": "deg",
          "symbol": "phi_II"
        }
      ],
      "result": {
        "value": 5.66,
        "unit": "1"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.7, таблица 5.5",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "table"
    },
    {
      "step_id": "k_z",
      "expression": "k_{z}=1",
      "substitutions": [],
      "result": {
        "value": 1.0,
        "unit": "1"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.7, экспликация k_z",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "step_id": "R",
      "expression": "R=\\frac{\\gamma_{c1}\\gamma_{c2}}{k}\\left[M_{\\gamma}k_{z}b\\gamma_{II}+M_{q}d_{1}\\gamma'_{II}+(M_{q}-1)d_{b}\\gamma'_{II}+M_{c}c_{II}\\right]",
      "substitutions": [
        {
          "value": 1.1,
          "unit": "1",
          "symbol": "gamma_c1"
        },
        {
          "value": 1.0,
          "unit": "1",
          "symbol": "gamma_c2"
        },
        {
          "value": 1.0,
          "unit": "1",
          "symbol": "k"
        },
        {
          "value": 0.51,
          "unit": "1",
          "symbol": "M_gamma"
        },
        {
          "value": 1.0,
          "unit": "1",
          "symbol": "k_z"
        },
        {
          "value": 2.0,
          "unit": "m",
          "symbol": "b"
        },
        {
          "value": 20.0,
          "unit": "kN/m3",
          "symbol": "gamma_II"
        },
        {
          "value": 3.06,
          "unit": "1",
          "symbol": "M_q"
        },
        {
          "value": 1.0,
          "unit": "m",
          "symbol": "d_1"
        },
        {
          "value": 20.0,
          "unit": "kN/m3",
          "symbol": "gamma_II_prime"
        },
        {
          "value": 0.0,
          "unit": "m",
          "symbol": "d_b"
        },
        {
          "value": 5.66,
          "unit": "1",
          "symbol": "M_c"
        },
        {
          "value": 10.0,
          "unit": "kPa",
          "symbol": "c_II"
        }
      ],
      "result": {
        "value": 152.02,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.7, формула (5.7)",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "kind": "engineer_formula",
      "step_id": "A",
      "expression": "A=b l",
      "substitutions": [
        {
          "value": 2.0,
          "unit": "m",
          "symbol": "b"
        },
        {
          "value": 3.0,
          "unit": "m",
          "symbol": "l"
        }
      ],
      "result": {
        "value": 6.0,
        "unit": "m2"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Геометрия прямоугольной подошвы: A=b*l, Wx=l*b²/6, Wy=b*l²/6; инженерный контракт 2026-11-08."
      }
    },
    {
      "kind": "engineer_formula",
      "step_id": "Wx",
      "expression": "W_x=l b^2/6",
      "substitutions": [
        {
          "value": 2.0,
          "unit": "m",
          "symbol": "b"
        },
        {
          "value": 3.0,
          "unit": "m",
          "symbol": "l"
        }
      ],
      "result": {
        "value": 2.0,
        "unit": "m3"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Геометрия прямоугольной подошвы: A=b*l, Wx=l*b²/6, Wy=b*l²/6; инженерный контракт 2026-11-08."
      }
    },
    {
      "kind": "engineer_formula",
      "step_id": "Wy",
      "expression": "W_y=b l^2/6",
      "substitutions": [
        {
          "value": 2.0,
          "unit": "m",
          "symbol": "b"
        },
        {
          "value": 3.0,
          "unit": "m",
          "symbol": "l"
        }
      ],
      "result": {
        "value": 3.0,
        "unit": "m3"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Геометрия прямоугольной подошвы: A=b*l, Wx=l*b²/6, Wy=b*l²/6; инженерный контракт 2026-11-08."
      }
    },
    {
      "kind": "engineer_formula",
      "step_id": "Mx_base",
      "expression": "M_{x,base}=M_x+Q_x h",
      "substitutions": [
        {
          "value": 40.0,
          "unit": "kN*m",
          "symbol": "Mx"
        },
        {
          "value": 20.0,
          "unit": "kN",
          "symbol": "Qx"
        },
        {
          "value": 1.0,
          "unit": "m",
          "symbol": "h"
        }
      ],
      "result": {
        "value": 60.0,
        "unit": "kN*m"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Подписанный перенос нагрузок к подошве M_base=M+Q*h; оси x=b и y=l; инженерный контракт 2026-11-08."
      }
    },
    {
      "kind": "engineer_formula",
      "step_id": "My_base",
      "expression": "M_{y,base}=M_y+Q_y h",
      "substitutions": [
        {
          "value": -30.0,
          "unit": "kN*m",
          "symbol": "My"
        },
        {
          "value": -15.0,
          "unit": "kN",
          "symbol": "Qy"
        },
        {
          "value": 1.0,
          "unit": "m",
          "symbol": "h"
        }
      ],
      "result": {
        "value": -45.0,
        "unit": "kN*m"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Подписанный перенос нагрузок к подошве M_base=M+Q*h; оси x=b и y=l; инженерный контракт 2026-11-08."
      }
    },
    {
      "step_id": "gamma_mt",
      "expression": "\\gamma_{mt}",
      "substitutions": [],
      "result": {
        "value": 20.0,
        "unit": "kN/m3"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.28, explanation of formula (5.11)",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "table"
    },
    {
      "step_id": "p",
      "expression": "p_{+}=\\frac{N}{A}+\\gamma_{mt}d+\\frac{M}{W}",
      "substitutions": [
        {
          "value": 600.0,
          "unit": "kN",
          "symbol": "N"
        },
        {
          "value": 6.0,
          "unit": "m2",
          "symbol": "A"
        },
        {
          "value": 20.0,
          "unit": "kN/m3",
          "symbol": "gamma_mt"
        },
        {
          "value": 1.0,
          "unit": "m",
          "symbol": "d"
        },
        {
          "value": 0.0,
          "unit": "kN*m",
          "symbol": "M"
        },
        {
          "value": 2.0,
          "unit": "m3",
          "symbol": "W"
        }
      ],
      "result": {
        "value": 120.0,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.28, formula (5.11)",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "kind": "engineer_formula",
      "step_id": "V",
      "expression": "V=N+\\gamma_{mt} d A",
      "substitutions": [
        {
          "value": 600.0,
          "unit": "kN",
          "symbol": "N"
        },
        {
          "value": 20.0,
          "unit": "kN/m3",
          "symbol": "gamma_mt"
        },
        {
          "value": 1.0,
          "unit": "m",
          "symbol": "d"
        },
        {
          "value": 6.0,
          "unit": "m2",
          "symbol": "A"
        }
      ],
      "result": {
        "value": 720.0,
        "unit": "kN"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08."
      }
    },
    {
      "step_id": "p_x_min",
      "expression": "p_{-}=\\frac{N}{A}+\\gamma_{mt}d-\\frac{M}{W}",
      "substitutions": [
        {
          "value": 600.0,
          "unit": "kN",
          "symbol": "N"
        },
        {
          "value": 6.0,
          "unit": "m2",
          "symbol": "A"
        },
        {
          "value": 20.0,
          "unit": "kN/m3",
          "symbol": "gamma_mt"
        },
        {
          "value": 1.0,
          "unit": "m",
          "symbol": "d"
        },
        {
          "value": 60.0,
          "unit": "kN*m",
          "symbol": "M"
        },
        {
          "value": 2.0,
          "unit": "m3",
          "symbol": "W"
        }
      ],
      "result": {
        "value": 90.0,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.28, formula (5.11)",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "step_id": "p_x_max",
      "expression": "p_{+}=\\frac{N}{A}+\\gamma_{mt}d+\\frac{M}{W}",
      "substitutions": [
        {
          "value": 600.0,
          "unit": "kN",
          "symbol": "N"
        },
        {
          "value": 6.0,
          "unit": "m2",
          "symbol": "A"
        },
        {
          "value": 20.0,
          "unit": "kN/m3",
          "symbol": "gamma_mt"
        },
        {
          "value": 1.0,
          "unit": "m",
          "symbol": "d"
        },
        {
          "value": 60.0,
          "unit": "kN*m",
          "symbol": "M"
        },
        {
          "value": 2.0,
          "unit": "m3",
          "symbol": "W"
        }
      ],
      "result": {
        "value": 150.0,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.28, formula (5.11)",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "kind": "engineer_formula",
      "step_id": "e_x",
      "expression": "e_x=|M_{x,base}|/V",
      "substitutions": [
        {
          "value": 60.0,
          "unit": "kN*m",
          "symbol": "Mx_base"
        },
        {
          "value": 720.0,
          "unit": "kN",
          "symbol": "V"
        }
      ],
      "result": {
        "value": 0.08333333333333333,
        "unit": "m"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08."
      }
    },
    {
      "step_id": "relative_eccentricity_x",
      "expression": "e/l\\leq1/6",
      "substitutions": [
        {
          "value": 0.041666666666666664,
          "unit": "1",
          "symbol": "e/L"
        },
        {
          "value": 1.0,
          "unit": "1",
          "symbol": "numerator"
        },
        {
          "value": 6.0,
          "unit": "1",
          "symbol": "denominator"
        }
      ],
      "result": {
        "value": 1.0,
        "unit": "1"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.28, applicability of formula (5.11)",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "step_id": "pressure_diagram_x",
      "expression": "e<l/6",
      "substitutions": [
        {
          "value": 0.08333333333333333,
          "unit": "m",
          "symbol": "e"
        },
        {
          "value": 2.0,
          "unit": "m",
          "symbol": "l"
        }
      ],
      "result": {
        "value": 0.08333333333333333,
        "unit": "m"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.27, figure 5.1",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "step_id": "p_y_min",
      "expression": "p_{-}=\\frac{N}{A}+\\gamma_{mt}d-\\frac{M}{W}",
      "substitutions": [
        {
          "value": 600.0,
          "unit": "kN",
          "symbol": "N"
        },
        {
          "value": 6.0,
          "unit": "m2",
          "symbol": "A"
        },
        {
          "value": 20.0,
          "unit": "kN/m3",
          "symbol": "gamma_mt"
        },
        {
          "value": 1.0,
          "unit": "m",
          "symbol": "d"
        },
        {
          "value": 45.0,
          "unit": "kN*m",
          "symbol": "M"
        },
        {
          "value": 3.0,
          "unit": "m3",
          "symbol": "W"
        }
      ],
      "result": {
        "value": 105.0,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.28, formula (5.11)",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "step_id": "p_y_max",
      "expression": "p_{+}=\\frac{N}{A}+\\gamma_{mt}d+\\frac{M}{W}",
      "substitutions": [
        {
          "value": 600.0,
          "unit": "kN",
          "symbol": "N"
        },
        {
          "value": 6.0,
          "unit": "m2",
          "symbol": "A"
        },
        {
          "value": 20.0,
          "unit": "kN/m3",
          "symbol": "gamma_mt"
        },
        {
          "value": 1.0,
          "unit": "m",
          "symbol": "d"
        },
        {
          "value": 45.0,
          "unit": "kN*m",
          "symbol": "M"
        },
        {
          "value": 3.0,
          "unit": "m3",
          "symbol": "W"
        }
      ],
      "result": {
        "value": 135.0,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.28, formula (5.11)",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "kind": "engineer_formula",
      "step_id": "e_y",
      "expression": "e_y=|M_{y,base}|/V",
      "substitutions": [
        {
          "value": -45.0,
          "unit": "kN*m",
          "symbol": "My_base"
        },
        {
          "value": 720.0,
          "unit": "kN",
          "symbol": "V"
        }
      ],
      "result": {
        "value": 0.0625,
        "unit": "m"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08."
      }
    },
    {
      "step_id": "relative_eccentricity_y",
      "expression": "e/l\\leq1/6",
      "substitutions": [
        {
          "value": 0.020833333333333332,
          "unit": "1",
          "symbol": "e/L"
        },
        {
          "value": 1.0,
          "unit": "1",
          "symbol": "numerator"
        },
        {
          "value": 6.0,
          "unit": "1",
          "symbol": "denominator"
        }
      ],
      "result": {
        "value": 1.0,
        "unit": "1"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.28, applicability of formula (5.11)",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "step_id": "pressure_diagram_y",
      "expression": "e<l/6",
      "substitutions": [
        {
          "value": 0.0625,
          "unit": "m",
          "symbol": "e"
        },
        {
          "value": 3.0,
          "unit": "m",
          "symbol": "l"
        }
      ],
      "result": {
        "value": 0.0625,
        "unit": "m"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.27, figure 5.1",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "step_id": "corner_component_pp",
      "expression": "P_{\\max}=\\frac{N}{A}+\\gamma_{mt}d+\\frac{M_x}{W_x}+\\frac{M_y}{W_y}",
      "substitutions": [
        {
          "value": 600.0,
          "unit": "kN",
          "symbol": "N"
        },
        {
          "value": 6.0,
          "unit": "m2",
          "symbol": "A"
        },
        {
          "value": 20.0,
          "unit": "kN/m3",
          "symbol": "gamma_mt"
        },
        {
          "value": 1.0,
          "unit": "m",
          "symbol": "d"
        },
        {
          "value": 60.0,
          "unit": "kN*m",
          "symbol": "M_x"
        },
        {
          "value": 2.0,
          "unit": "m3",
          "symbol": "W_x"
        },
        {
          "value": -45.0,
          "unit": "kN*m",
          "symbol": "M_y"
        },
        {
          "value": 3.0,
          "unit": "m3",
          "symbol": "W_y"
        }
      ],
      "result": {
        "value": 135.0,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.29, formula (5.15)",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "kind": "engineer_formula",
      "step_id": "p_corner_pp",
      "expression": "p_{pp}=p+s_x M_{x,base}/W_x+s_y M_{y,base}/W_y",
      "substitutions": [
        {
          "value": 120.0,
          "unit": "kPa",
          "symbol": "p"
        },
        {
          "value": 60.0,
          "unit": "kN*m",
          "symbol": "Mx_base"
        },
        {
          "value": 2.0,
          "unit": "m3",
          "symbol": "Wx"
        },
        {
          "value": -45.0,
          "unit": "kN*m",
          "symbol": "My_base"
        },
        {
          "value": 3.0,
          "unit": "m3",
          "symbol": "Wy"
        },
        {
          "value": 1.0,
          "unit": "1",
          "symbol": "sign_x_pp"
        },
        {
          "value": 1.0,
          "unit": "1",
          "symbol": "sign_y_pp"
        },
        {
          "value": 135.0,
          "unit": "kPa",
          "symbol": "corner_component_pp"
        }
      ],
      "result": {
        "value": 135.0,
        "unit": "kPa"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08."
      }
    },
    {
      "step_id": "corner_component_pm",
      "expression": "P_{\\max}=\\frac{N}{A}+\\gamma_{mt}d+\\frac{M_x}{W_x}+\\frac{M_y}{W_y}",
      "substitutions": [
        {
          "value": 600.0,
          "unit": "kN",
          "symbol": "N"
        },
        {
          "value": 6.0,
          "unit": "m2",
          "symbol": "A"
        },
        {
          "value": 20.0,
          "unit": "kN/m3",
          "symbol": "gamma_mt"
        },
        {
          "value": 1.0,
          "unit": "m",
          "symbol": "d"
        },
        {
          "value": 60.0,
          "unit": "kN*m",
          "symbol": "M_x"
        },
        {
          "value": 2.0,
          "unit": "m3",
          "symbol": "W_x"
        },
        {
          "value": 45.0,
          "unit": "kN*m",
          "symbol": "M_y"
        },
        {
          "value": 3.0,
          "unit": "m3",
          "symbol": "W_y"
        }
      ],
      "result": {
        "value": 165.0,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.29, formula (5.15)",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "kind": "engineer_formula",
      "step_id": "p_corner_pm",
      "expression": "p_{pm}=p+s_x M_{x,base}/W_x+s_y M_{y,base}/W_y",
      "substitutions": [
        {
          "value": 120.0,
          "unit": "kPa",
          "symbol": "p"
        },
        {
          "value": 60.0,
          "unit": "kN*m",
          "symbol": "Mx_base"
        },
        {
          "value": 2.0,
          "unit": "m3",
          "symbol": "Wx"
        },
        {
          "value": -45.0,
          "unit": "kN*m",
          "symbol": "My_base"
        },
        {
          "value": 3.0,
          "unit": "m3",
          "symbol": "Wy"
        },
        {
          "value": 1.0,
          "unit": "1",
          "symbol": "sign_x_pm"
        },
        {
          "value": -1.0,
          "unit": "1",
          "symbol": "sign_y_pm"
        },
        {
          "value": 165.0,
          "unit": "kPa",
          "symbol": "corner_component_pm"
        }
      ],
      "result": {
        "value": 165.0,
        "unit": "kPa"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08."
      }
    },
    {
      "step_id": "corner_component_mp",
      "expression": "P_{\\max}=\\frac{N}{A}+\\gamma_{mt}d+\\frac{M_x}{W_x}+\\frac{M_y}{W_y}",
      "substitutions": [
        {
          "value": 600.0,
          "unit": "kN",
          "symbol": "N"
        },
        {
          "value": 6.0,
          "unit": "m2",
          "symbol": "A"
        },
        {
          "value": 20.0,
          "unit": "kN/m3",
          "symbol": "gamma_mt"
        },
        {
          "value": 1.0,
          "unit": "m",
          "symbol": "d"
        },
        {
          "value": -60.0,
          "unit": "kN*m",
          "symbol": "M_x"
        },
        {
          "value": 2.0,
          "unit": "m3",
          "symbol": "W_x"
        },
        {
          "value": -45.0,
          "unit": "kN*m",
          "symbol": "M_y"
        },
        {
          "value": 3.0,
          "unit": "m3",
          "symbol": "W_y"
        }
      ],
      "result": {
        "value": 75.0,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.29, formula (5.15)",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "kind": "engineer_formula",
      "step_id": "p_corner_mp",
      "expression": "p_{mp}=p+s_x M_{x,base}/W_x+s_y M_{y,base}/W_y",
      "substitutions": [
        {
          "value": 120.0,
          "unit": "kPa",
          "symbol": "p"
        },
        {
          "value": 60.0,
          "unit": "kN*m",
          "symbol": "Mx_base"
        },
        {
          "value": 2.0,
          "unit": "m3",
          "symbol": "Wx"
        },
        {
          "value": -45.0,
          "unit": "kN*m",
          "symbol": "My_base"
        },
        {
          "value": 3.0,
          "unit": "m3",
          "symbol": "Wy"
        },
        {
          "value": -1.0,
          "unit": "1",
          "symbol": "sign_x_mp"
        },
        {
          "value": 1.0,
          "unit": "1",
          "symbol": "sign_y_mp"
        },
        {
          "value": 75.0,
          "unit": "kPa",
          "symbol": "corner_component_mp"
        }
      ],
      "result": {
        "value": 75.0,
        "unit": "kPa"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08."
      }
    },
    {
      "step_id": "corner_component_mm",
      "expression": "P_{\\max}=\\frac{N}{A}+\\gamma_{mt}d+\\frac{M_x}{W_x}+\\frac{M_y}{W_y}",
      "substitutions": [
        {
          "value": 600.0,
          "unit": "kN",
          "symbol": "N"
        },
        {
          "value": 6.0,
          "unit": "m2",
          "symbol": "A"
        },
        {
          "value": 20.0,
          "unit": "kN/m3",
          "symbol": "gamma_mt"
        },
        {
          "value": 1.0,
          "unit": "m",
          "symbol": "d"
        },
        {
          "value": -60.0,
          "unit": "kN*m",
          "symbol": "M_x"
        },
        {
          "value": 2.0,
          "unit": "m3",
          "symbol": "W_x"
        },
        {
          "value": 45.0,
          "unit": "kN*m",
          "symbol": "M_y"
        },
        {
          "value": 3.0,
          "unit": "m3",
          "symbol": "W_y"
        }
      ],
      "result": {
        "value": 105.0,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.29, formula (5.15)",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "kind": "engineer_formula",
      "step_id": "p_corner_mm",
      "expression": "p_{mm}=p+s_x M_{x,base}/W_x+s_y M_{y,base}/W_y",
      "substitutions": [
        {
          "value": 120.0,
          "unit": "kPa",
          "symbol": "p"
        },
        {
          "value": 60.0,
          "unit": "kN*m",
          "symbol": "Mx_base"
        },
        {
          "value": 2.0,
          "unit": "m3",
          "symbol": "Wx"
        },
        {
          "value": -45.0,
          "unit": "kN*m",
          "symbol": "My_base"
        },
        {
          "value": 3.0,
          "unit": "m3",
          "symbol": "Wy"
        },
        {
          "value": -1.0,
          "unit": "1",
          "symbol": "sign_x_mm"
        },
        {
          "value": -1.0,
          "unit": "1",
          "symbol": "sign_y_mm"
        },
        {
          "value": 105.0,
          "unit": "kPa",
          "symbol": "corner_component_mm"
        }
      ],
      "result": {
        "value": 105.0,
        "unit": "kPa"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08."
      }
    },
    {
      "kind": "engineer_formula",
      "step_id": "p_corner_min",
      "expression": "p_{corner,min}=\\min(p_{++},p_{+-},p_{-+},p_{--})",
      "substitutions": [
        {
          "value": 135.0,
          "unit": "kPa",
          "symbol": "p_corner_pp"
        },
        {
          "value": 165.0,
          "unit": "kPa",
          "symbol": "p_corner_pm"
        },
        {
          "value": 75.0,
          "unit": "kPa",
          "symbol": "p_corner_mp"
        },
        {
          "value": 105.0,
          "unit": "kPa",
          "symbol": "p_corner_mm"
        }
      ],
      "result": {
        "value": 75.0,
        "unit": "kPa"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Полный контакт прямоугольной подошвы: минимум четырёх подписанных угловых давлений неотрицателен; решение инженера 2026-11-08."
      }
    },
    {
      "kind": "engineer_formula",
      "step_id": "p_corner_max",
      "expression": "p_{corner,max}=\\max(p_{++},p_{+-},p_{-+},p_{--})",
      "substitutions": [
        {
          "value": 135.0,
          "unit": "kPa",
          "symbol": "p_corner_pp"
        },
        {
          "value": 165.0,
          "unit": "kPa",
          "symbol": "p_corner_pm"
        },
        {
          "value": 75.0,
          "unit": "kPa",
          "symbol": "p_corner_mp"
        },
        {
          "value": 105.0,
          "unit": "kPa",
          "symbol": "p_corner_mm"
        }
      ],
      "result": {
        "value": 165.0,
        "unit": "kPa"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08."
      }
    },
    {
      "step_id": "edge_limit_multiplier",
      "expression": "edge_limit_multiplier",
      "substitutions": [],
      "result": {
        "value": 1.2,
        "unit": "1"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.26",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "table"
    },
    {
      "step_id": "edge_limit",
      "expression": "p_{edge,lim}=\\lambda_e R",
      "substitutions": [
        {
          "value": 1.2,
          "unit": "1",
          "symbol": "edge_limit_multiplier"
        },
        {
          "value": 152.02,
          "unit": "kPa",
          "symbol": "R"
        }
      ],
      "result": {
        "value": 182.424,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.26",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "step_id": "corner_limit_multiplier",
      "expression": "corner_limit_multiplier",
      "substitutions": [],
      "result": {
        "value": 1.5,
        "unit": "1"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.26",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "table"
    },
    {
      "step_id": "corner_limit",
      "expression": "p_{corner,lim}=\\lambda_c R",
      "substitutions": [
        {
          "value": 1.5,
          "unit": "1",
          "symbol": "corner_limit_multiplier"
        },
        {
          "value": 152.02,
          "unit": "kPa",
          "symbol": "R"
        }
      ],
      "result": {
        "value": 228.03000000000003,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.26",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "step_id": "p_le_R",
      "expression": "p \\le R",
      "substitutions": [
        {
          "value": 120.0,
          "unit": "kPa",
          "symbol": "p"
        },
        {
          "value": 152.02,
          "unit": "kPa",
          "symbol": "R"
        }
      ],
      "result": {
        "value": 120.0,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.7",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "check",
      "operator": "le",
      "right": {
        "value": 152.02,
        "unit": "kPa"
      },
      "passed": true
    },
    {
      "step_id": "p_x_max_le_limit",
      "expression": "p_x_max \\le edge_limit",
      "substitutions": [
        {
          "value": 150.0,
          "unit": "kPa",
          "symbol": "p_x_max"
        },
        {
          "value": 182.424,
          "unit": "kPa",
          "symbol": "edge_limit"
        }
      ],
      "result": {
        "value": 150.0,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.26",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "check",
      "operator": "le",
      "right": {
        "value": 182.424,
        "unit": "kPa"
      },
      "passed": true
    },
    {
      "step_id": "p_y_max_le_limit",
      "expression": "p_y_max \\le edge_limit",
      "substitutions": [
        {
          "value": 135.0,
          "unit": "kPa",
          "symbol": "p_y_max"
        },
        {
          "value": 182.424,
          "unit": "kPa",
          "symbol": "edge_limit"
        }
      ],
      "result": {
        "value": 135.0,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.26",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "check",
      "operator": "le",
      "right": {
        "value": 182.424,
        "unit": "kPa"
      },
      "passed": true
    },
    {
      "step_id": "p_corner_max_le_limit",
      "expression": "p_corner_max \\le corner_limit",
      "substitutions": [
        {
          "value": 165.0,
          "unit": "kPa",
          "symbol": "p_corner_max"
        },
        {
          "value": 228.03000000000003,
          "unit": "kPa",
          "symbol": "corner_limit"
        }
      ],
      "result": {
        "value": 165.0,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.26",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "check",
      "operator": "le",
      "right": {
        "value": 228.03000000000003,
        "unit": "kPa"
      },
      "passed": true
    }
  ],
  "unverified_step_count": 30,
  "result_id": "77777777-7777-4777-8777-777777777777",
  "parameter_source": {
    "kind": "interim",
    "data_sha256": "faaa0724af57ca6c8066f558c4e75c2785d099b34cbfb07c4a85892fdc3b68fe", // pragma: allowlist secret
    "profile": "strict"
  }
} satisfies ResultEnvelope

export const loadsBiaxialJson = "{\"engine_version\":\"0.1.0\",\"input_hash\":\"75aea1a6c3764d8ed86f3e35f8b54a8aaa352d71e0b8e2b3228d08fa83e0eb6d\",\"outputs\":[{\"value\":152.02,\"unit\":\"kPa\",\"quantity\":\"R\",\"rounding_rule\":{\"decimals\":2,\"mode\":\"half_up\"},\"rounding_source\":{\"engineer\":\"Аким\",\"rationale\":\"Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются.\"}},{\"value\":120.0,\"unit\":\"kPa\",\"quantity\":\"p\",\"rounding_rule\":{\"decimals\":2,\"mode\":\"half_up\"},\"rounding_source\":{\"engineer\":\"Аким\",\"rationale\":\"Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются.\"}},{\"value\":90.0,\"unit\":\"kPa\",\"quantity\":\"p_x_min\",\"rounding_rule\":{\"decimals\":2,\"mode\":\"half_up\"},\"rounding_source\":{\"engineer\":\"Аким\",\"rationale\":\"Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются.\"}},{\"value\":150.0,\"unit\":\"kPa\",\"quantity\":\"p_x_max\",\"rounding_rule\":{\"decimals\":2,\"mode\":\"half_up\"},\"rounding_source\":{\"engineer\":\"Аким\",\"rationale\":\"Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются.\"}},{\"value\":105.0,\"unit\":\"kPa\",\"quantity\":\"p_y_min\",\"rounding_rule\":{\"decimals\":2,\"mode\":\"half_up\"},\"rounding_source\":{\"engineer\":\"Аким\",\"rationale\":\"Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются.\"}},{\"value\":135.0,\"unit\":\"kPa\",\"quantity\":\"p_y_max\",\"rounding_rule\":{\"decimals\":2,\"mode\":\"half_up\"},\"rounding_source\":{\"engineer\":\"Аким\",\"rationale\":\"Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются.\"}},{\"value\":135.0,\"unit\":\"kPa\",\"quantity\":\"p_corner_pp\",\"rounding_rule\":{\"decimals\":2,\"mode\":\"half_up\"},\"rounding_source\":{\"engineer\":\"Аким\",\"rationale\":\"Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются.\"}},{\"value\":165.0,\"unit\":\"kPa\",\"quantity\":\"p_corner_pm\",\"rounding_rule\":{\"decimals\":2,\"mode\":\"half_up\"},\"rounding_source\":{\"engineer\":\"Аким\",\"rationale\":\"Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются.\"}},{\"value\":75.0,\"unit\":\"kPa\",\"quantity\":\"p_corner_mp\",\"rounding_rule\":{\"decimals\":2,\"mode\":\"half_up\"},\"rounding_source\":{\"engineer\":\"Аким\",\"rationale\":\"Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются.\"}},{\"value\":105.0,\"unit\":\"kPa\",\"quantity\":\"p_corner_mm\",\"rounding_rule\":{\"decimals\":2,\"mode\":\"half_up\"},\"rounding_source\":{\"engineer\":\"Аким\",\"rationale\":\"Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются.\"}}],\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7, таблица 5.4\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"},{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7, экспликация k\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"},{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7, таблица 5.5\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"},{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7, экспликация k_z\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"},{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7, формула (5.7)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"},{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.28, explanation of formula (5.11)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"},{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.28, formula (5.11)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"},{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.28, applicability of formula (5.11)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"},{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.27, figure 5.1\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"},{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.29, formula (5.15)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"},{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.26\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"},{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"engineer_rules\":[{\"engineer\":\"Аким\",\"rationale\":\"Геометрия прямоугольной подошвы: A=b*l, Wx=l*b²/6, Wy=b*l²/6; инженерный контракт 2026-11-08.\"},{\"engineer\":\"Аким\",\"rationale\":\"Подписанный перенос нагрузок к подошве M_base=M+Q*h; оси x=b и y=l; инженерный контракт 2026-11-08.\"},{\"engineer\":\"Аким\",\"rationale\":\"Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08.\"},{\"engineer\":\"Аким\",\"rationale\":\"Полный контакт прямоугольной подошвы: минимум четырёх подписанных угловых давлений неотрицателен; решение инженера 2026-11-08.\"},{\"engineer\":\"Аким\",\"rationale\":\"Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются.\"}],\"verdict\":\"pass\",\"verdict_reason\":{\"kind\":\"check\",\"step_id\":\"p_corner_max_le_limit\"},\"warnings\":[],\"trace\":[{\"step_id\":\"gamma_c1\",\"expression\":\"\\\\gamma_{c1}\",\"substitutions\":[],\"result\":{\"value\":1.1,\"unit\":\"1\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7, таблица 5.4\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"table\"},{\"step_id\":\"gamma_c2\",\"expression\":\"\\\\gamma_{c2}\",\"substitutions\":[],\"result\":{\"value\":1.0,\"unit\":\"1\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7, таблица 5.4\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"table\"},{\"step_id\":\"k\",\"expression\":\"k\",\"substitutions\":[],\"result\":{\"value\":1.0,\"unit\":\"1\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7, экспликация k\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"table\"},{\"step_id\":\"M_gamma\",\"expression\":\"M_{\\\\gamma} = M_{\\\\gamma}\\\\left(\\\\varphi_{II}\\\\right)\",\"substitutions\":[{\"value\":20.0,\"unit\":\"deg\",\"symbol\":\"phi_II\"}],\"result\":{\"value\":0.51,\"unit\":\"1\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7, таблица 5.5\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"table\"},{\"step_id\":\"M_q\",\"expression\":\"M_{q} = M_{q}\\\\left(\\\\varphi_{II}\\\\right)\",\"substitutions\":[{\"value\":20.0,\"unit\":\"deg\",\"symbol\":\"phi_II\"}],\"result\":{\"value\":3.06,\"unit\":\"1\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7, таблица 5.5\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"table\"},{\"step_id\":\"M_c\",\"expression\":\"M_{c} = M_{c}\\\\left(\\\\varphi_{II}\\\\right)\",\"substitutions\":[{\"value\":20.0,\"unit\":\"deg\",\"symbol\":\"phi_II\"}],\"result\":{\"value\":5.66,\"unit\":\"1\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7, таблица 5.5\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"table\"},{\"step_id\":\"k_z\",\"expression\":\"k_{z}=1\",\"substitutions\":[],\"result\":{\"value\":1.0,\"unit\":\"1\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7, экспликация k_z\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"step_id\":\"R\",\"expression\":\"R=\\\\frac{\\\\gamma_{c1}\\\\gamma_{c2}}{k}\\\\left[M_{\\\\gamma}k_{z}b\\\\gamma_{II}+M_{q}d_{1}\\\\gamma'_{II}+(M_{q}-1)d_{b}\\\\gamma'_{II}+M_{c}c_{II}\\\\right]\",\"substitutions\":[{\"value\":1.1,\"unit\":\"1\",\"symbol\":\"gamma_c1\"},{\"value\":1.0,\"unit\":\"1\",\"symbol\":\"gamma_c2\"},{\"value\":1.0,\"unit\":\"1\",\"symbol\":\"k\"},{\"value\":0.51,\"unit\":\"1\",\"symbol\":\"M_gamma\"},{\"value\":1.0,\"unit\":\"1\",\"symbol\":\"k_z\"},{\"value\":2.0,\"unit\":\"m\",\"symbol\":\"b\"},{\"value\":20.0,\"unit\":\"kN/m3\",\"symbol\":\"gamma_II\"},{\"value\":3.06,\"unit\":\"1\",\"symbol\":\"M_q\"},{\"value\":1.0,\"unit\":\"m\",\"symbol\":\"d_1\"},{\"value\":20.0,\"unit\":\"kN/m3\",\"symbol\":\"gamma_II_prime\"},{\"value\":0.0,\"unit\":\"m\",\"symbol\":\"d_b\"},{\"value\":5.66,\"unit\":\"1\",\"symbol\":\"M_c\"},{\"value\":10.0,\"unit\":\"kPa\",\"symbol\":\"c_II\"}],\"result\":{\"value\":152.02,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7, формула (5.7)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"kind\":\"engineer_formula\",\"step_id\":\"A\",\"expression\":\"A=b l\",\"substitutions\":[{\"value\":2.0,\"unit\":\"m\",\"symbol\":\"b\"},{\"value\":3.0,\"unit\":\"m\",\"symbol\":\"l\"}],\"result\":{\"value\":6.0,\"unit\":\"m2\"},\"source\":{\"engineer\":\"Аким\",\"rationale\":\"Геометрия прямоугольной подошвы: A=b*l, Wx=l*b²/6, Wy=b*l²/6; инженерный контракт 2026-11-08.\"}},{\"kind\":\"engineer_formula\",\"step_id\":\"Wx\",\"expression\":\"W_x=l b^2/6\",\"substitutions\":[{\"value\":2.0,\"unit\":\"m\",\"symbol\":\"b\"},{\"value\":3.0,\"unit\":\"m\",\"symbol\":\"l\"}],\"result\":{\"value\":2.0,\"unit\":\"m3\"},\"source\":{\"engineer\":\"Аким\",\"rationale\":\"Геометрия прямоугольной подошвы: A=b*l, Wx=l*b²/6, Wy=b*l²/6; инженерный контракт 2026-11-08.\"}},{\"kind\":\"engineer_formula\",\"step_id\":\"Wy\",\"expression\":\"W_y=b l^2/6\",\"substitutions\":[{\"value\":2.0,\"unit\":\"m\",\"symbol\":\"b\"},{\"value\":3.0,\"unit\":\"m\",\"symbol\":\"l\"}],\"result\":{\"value\":3.0,\"unit\":\"m3\"},\"source\":{\"engineer\":\"Аким\",\"rationale\":\"Геометрия прямоугольной подошвы: A=b*l, Wx=l*b²/6, Wy=b*l²/6; инженерный контракт 2026-11-08.\"}},{\"kind\":\"engineer_formula\",\"step_id\":\"Mx_base\",\"expression\":\"M_{x,base}=M_x+Q_x h\",\"substitutions\":[{\"value\":40.0,\"unit\":\"kN*m\",\"symbol\":\"Mx\"},{\"value\":20.0,\"unit\":\"kN\",\"symbol\":\"Qx\"},{\"value\":1.0,\"unit\":\"m\",\"symbol\":\"h\"}],\"result\":{\"value\":60.0,\"unit\":\"kN*m\"},\"source\":{\"engineer\":\"Аким\",\"rationale\":\"Подписанный перенос нагрузок к подошве M_base=M+Q*h; оси x=b и y=l; инженерный контракт 2026-11-08.\"}},{\"kind\":\"engineer_formula\",\"step_id\":\"My_base\",\"expression\":\"M_{y,base}=M_y+Q_y h\",\"substitutions\":[{\"value\":-30.0,\"unit\":\"kN*m\",\"symbol\":\"My\"},{\"value\":-15.0,\"unit\":\"kN\",\"symbol\":\"Qy\"},{\"value\":1.0,\"unit\":\"m\",\"symbol\":\"h\"}],\"result\":{\"value\":-45.0,\"unit\":\"kN*m\"},\"source\":{\"engineer\":\"Аким\",\"rationale\":\"Подписанный перенос нагрузок к подошве M_base=M+Q*h; оси x=b и y=l; инженерный контракт 2026-11-08.\"}},{\"step_id\":\"gamma_mt\",\"expression\":\"\\\\gamma_{mt}\",\"substitutions\":[],\"result\":{\"value\":20.0,\"unit\":\"kN/m3\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.28, explanation of formula (5.11)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"table\"},{\"step_id\":\"p\",\"expression\":\"p_{+}=\\\\frac{N}{A}+\\\\gamma_{mt}d+\\\\frac{M}{W}\",\"substitutions\":[{\"value\":600.0,\"unit\":\"kN\",\"symbol\":\"N\"},{\"value\":6.0,\"unit\":\"m2\",\"symbol\":\"A\"},{\"value\":20.0,\"unit\":\"kN/m3\",\"symbol\":\"gamma_mt\"},{\"value\":1.0,\"unit\":\"m\",\"symbol\":\"d\"},{\"value\":0.0,\"unit\":\"kN*m\",\"symbol\":\"M\"},{\"value\":2.0,\"unit\":\"m3\",\"symbol\":\"W\"}],\"result\":{\"value\":120.0,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.28, formula (5.11)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"kind\":\"engineer_formula\",\"step_id\":\"V\",\"expression\":\"V=N+\\\\gamma_{mt} d A\",\"substitutions\":[{\"value\":600.0,\"unit\":\"kN\",\"symbol\":\"N\"},{\"value\":20.0,\"unit\":\"kN/m3\",\"symbol\":\"gamma_mt\"},{\"value\":1.0,\"unit\":\"m\",\"symbol\":\"d\"},{\"value\":6.0,\"unit\":\"m2\",\"symbol\":\"A\"}],\"result\":{\"value\":720.0,\"unit\":\"kN\"},\"source\":{\"engineer\":\"Аким\",\"rationale\":\"Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08.\"}},{\"step_id\":\"p_x_min\",\"expression\":\"p_{-}=\\\\frac{N}{A}+\\\\gamma_{mt}d-\\\\frac{M}{W}\",\"substitutions\":[{\"value\":600.0,\"unit\":\"kN\",\"symbol\":\"N\"},{\"value\":6.0,\"unit\":\"m2\",\"symbol\":\"A\"},{\"value\":20.0,\"unit\":\"kN/m3\",\"symbol\":\"gamma_mt\"},{\"value\":1.0,\"unit\":\"m\",\"symbol\":\"d\"},{\"value\":60.0,\"unit\":\"kN*m\",\"symbol\":\"M\"},{\"value\":2.0,\"unit\":\"m3\",\"symbol\":\"W\"}],\"result\":{\"value\":90.0,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.28, formula (5.11)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"step_id\":\"p_x_max\",\"expression\":\"p_{+}=\\\\frac{N}{A}+\\\\gamma_{mt}d+\\\\frac{M}{W}\",\"substitutions\":[{\"value\":600.0,\"unit\":\"kN\",\"symbol\":\"N\"},{\"value\":6.0,\"unit\":\"m2\",\"symbol\":\"A\"},{\"value\":20.0,\"unit\":\"kN/m3\",\"symbol\":\"gamma_mt\"},{\"value\":1.0,\"unit\":\"m\",\"symbol\":\"d\"},{\"value\":60.0,\"unit\":\"kN*m\",\"symbol\":\"M\"},{\"value\":2.0,\"unit\":\"m3\",\"symbol\":\"W\"}],\"result\":{\"value\":150.0,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.28, formula (5.11)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"kind\":\"engineer_formula\",\"step_id\":\"e_x\",\"expression\":\"e_x=|M_{x,base}|/V\",\"substitutions\":[{\"value\":60.0,\"unit\":\"kN*m\",\"symbol\":\"Mx_base\"},{\"value\":720.0,\"unit\":\"kN\",\"symbol\":\"V\"}],\"result\":{\"value\":0.08333333333333333,\"unit\":\"m\"},\"source\":{\"engineer\":\"Аким\",\"rationale\":\"Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08.\"}},{\"step_id\":\"relative_eccentricity_x\",\"expression\":\"e/l\\\\leq1/6\",\"substitutions\":[{\"value\":0.041666666666666664,\"unit\":\"1\",\"symbol\":\"e/L\"},{\"value\":1.0,\"unit\":\"1\",\"symbol\":\"numerator\"},{\"value\":6.0,\"unit\":\"1\",\"symbol\":\"denominator\"}],\"result\":{\"value\":1.0,\"unit\":\"1\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.28, applicability of formula (5.11)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"step_id\":\"pressure_diagram_x\",\"expression\":\"e<l/6\",\"substitutions\":[{\"value\":0.08333333333333333,\"unit\":\"m\",\"symbol\":\"e\"},{\"value\":2.0,\"unit\":\"m\",\"symbol\":\"l\"}],\"result\":{\"value\":0.08333333333333333,\"unit\":\"m\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.27, figure 5.1\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"step_id\":\"p_y_min\",\"expression\":\"p_{-}=\\\\frac{N}{A}+\\\\gamma_{mt}d-\\\\frac{M}{W}\",\"substitutions\":[{\"value\":600.0,\"unit\":\"kN\",\"symbol\":\"N\"},{\"value\":6.0,\"unit\":\"m2\",\"symbol\":\"A\"},{\"value\":20.0,\"unit\":\"kN/m3\",\"symbol\":\"gamma_mt\"},{\"value\":1.0,\"unit\":\"m\",\"symbol\":\"d\"},{\"value\":45.0,\"unit\":\"kN*m\",\"symbol\":\"M\"},{\"value\":3.0,\"unit\":\"m3\",\"symbol\":\"W\"}],\"result\":{\"value\":105.0,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.28, formula (5.11)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"step_id\":\"p_y_max\",\"expression\":\"p_{+}=\\\\frac{N}{A}+\\\\gamma_{mt}d+\\\\frac{M}{W}\",\"substitutions\":[{\"value\":600.0,\"unit\":\"kN\",\"symbol\":\"N\"},{\"value\":6.0,\"unit\":\"m2\",\"symbol\":\"A\"},{\"value\":20.0,\"unit\":\"kN/m3\",\"symbol\":\"gamma_mt\"},{\"value\":1.0,\"unit\":\"m\",\"symbol\":\"d\"},{\"value\":45.0,\"unit\":\"kN*m\",\"symbol\":\"M\"},{\"value\":3.0,\"unit\":\"m3\",\"symbol\":\"W\"}],\"result\":{\"value\":135.0,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.28, formula (5.11)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"kind\":\"engineer_formula\",\"step_id\":\"e_y\",\"expression\":\"e_y=|M_{y,base}|/V\",\"substitutions\":[{\"value\":-45.0,\"unit\":\"kN*m\",\"symbol\":\"My_base\"},{\"value\":720.0,\"unit\":\"kN\",\"symbol\":\"V\"}],\"result\":{\"value\":0.0625,\"unit\":\"m\"},\"source\":{\"engineer\":\"Аким\",\"rationale\":\"Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08.\"}},{\"step_id\":\"relative_eccentricity_y\",\"expression\":\"e/l\\\\leq1/6\",\"substitutions\":[{\"value\":0.020833333333333332,\"unit\":\"1\",\"symbol\":\"e/L\"},{\"value\":1.0,\"unit\":\"1\",\"symbol\":\"numerator\"},{\"value\":6.0,\"unit\":\"1\",\"symbol\":\"denominator\"}],\"result\":{\"value\":1.0,\"unit\":\"1\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.28, applicability of formula (5.11)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"step_id\":\"pressure_diagram_y\",\"expression\":\"e<l/6\",\"substitutions\":[{\"value\":0.0625,\"unit\":\"m\",\"symbol\":\"e\"},{\"value\":3.0,\"unit\":\"m\",\"symbol\":\"l\"}],\"result\":{\"value\":0.0625,\"unit\":\"m\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.27, figure 5.1\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"step_id\":\"corner_component_pp\",\"expression\":\"P_{\\\\max}=\\\\frac{N}{A}+\\\\gamma_{mt}d+\\\\frac{M_x}{W_x}+\\\\frac{M_y}{W_y}\",\"substitutions\":[{\"value\":600.0,\"unit\":\"kN\",\"symbol\":\"N\"},{\"value\":6.0,\"unit\":\"m2\",\"symbol\":\"A\"},{\"value\":20.0,\"unit\":\"kN/m3\",\"symbol\":\"gamma_mt\"},{\"value\":1.0,\"unit\":\"m\",\"symbol\":\"d\"},{\"value\":60.0,\"unit\":\"kN*m\",\"symbol\":\"M_x\"},{\"value\":2.0,\"unit\":\"m3\",\"symbol\":\"W_x\"},{\"value\":-45.0,\"unit\":\"kN*m\",\"symbol\":\"M_y\"},{\"value\":3.0,\"unit\":\"m3\",\"symbol\":\"W_y\"}],\"result\":{\"value\":135.0,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.29, formula (5.15)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"kind\":\"engineer_formula\",\"step_id\":\"p_corner_pp\",\"expression\":\"p_{pp}=p+s_x M_{x,base}/W_x+s_y M_{y,base}/W_y\",\"substitutions\":[{\"value\":120.0,\"unit\":\"kPa\",\"symbol\":\"p\"},{\"value\":60.0,\"unit\":\"kN*m\",\"symbol\":\"Mx_base\"},{\"value\":2.0,\"unit\":\"m3\",\"symbol\":\"Wx\"},{\"value\":-45.0,\"unit\":\"kN*m\",\"symbol\":\"My_base\"},{\"value\":3.0,\"unit\":\"m3\",\"symbol\":\"Wy\"},{\"value\":1.0,\"unit\":\"1\",\"symbol\":\"sign_x_pp\"},{\"value\":1.0,\"unit\":\"1\",\"symbol\":\"sign_y_pp\"},{\"value\":135.0,\"unit\":\"kPa\",\"symbol\":\"corner_component_pp\"}],\"result\":{\"value\":135.0,\"unit\":\"kPa\"},\"source\":{\"engineer\":\"Аким\",\"rationale\":\"Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08.\"}},{\"step_id\":\"corner_component_pm\",\"expression\":\"P_{\\\\max}=\\\\frac{N}{A}+\\\\gamma_{mt}d+\\\\frac{M_x}{W_x}+\\\\frac{M_y}{W_y}\",\"substitutions\":[{\"value\":600.0,\"unit\":\"kN\",\"symbol\":\"N\"},{\"value\":6.0,\"unit\":\"m2\",\"symbol\":\"A\"},{\"value\":20.0,\"unit\":\"kN/m3\",\"symbol\":\"gamma_mt\"},{\"value\":1.0,\"unit\":\"m\",\"symbol\":\"d\"},{\"value\":60.0,\"unit\":\"kN*m\",\"symbol\":\"M_x\"},{\"value\":2.0,\"unit\":\"m3\",\"symbol\":\"W_x\"},{\"value\":45.0,\"unit\":\"kN*m\",\"symbol\":\"M_y\"},{\"value\":3.0,\"unit\":\"m3\",\"symbol\":\"W_y\"}],\"result\":{\"value\":165.0,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.29, formula (5.15)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"kind\":\"engineer_formula\",\"step_id\":\"p_corner_pm\",\"expression\":\"p_{pm}=p+s_x M_{x,base}/W_x+s_y M_{y,base}/W_y\",\"substitutions\":[{\"value\":120.0,\"unit\":\"kPa\",\"symbol\":\"p\"},{\"value\":60.0,\"unit\":\"kN*m\",\"symbol\":\"Mx_base\"},{\"value\":2.0,\"unit\":\"m3\",\"symbol\":\"Wx\"},{\"value\":-45.0,\"unit\":\"kN*m\",\"symbol\":\"My_base\"},{\"value\":3.0,\"unit\":\"m3\",\"symbol\":\"Wy\"},{\"value\":1.0,\"unit\":\"1\",\"symbol\":\"sign_x_pm\"},{\"value\":-1.0,\"unit\":\"1\",\"symbol\":\"sign_y_pm\"},{\"value\":165.0,\"unit\":\"kPa\",\"symbol\":\"corner_component_pm\"}],\"result\":{\"value\":165.0,\"unit\":\"kPa\"},\"source\":{\"engineer\":\"Аким\",\"rationale\":\"Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08.\"}},{\"step_id\":\"corner_component_mp\",\"expression\":\"P_{\\\\max}=\\\\frac{N}{A}+\\\\gamma_{mt}d+\\\\frac{M_x}{W_x}+\\\\frac{M_y}{W_y}\",\"substitutions\":[{\"value\":600.0,\"unit\":\"kN\",\"symbol\":\"N\"},{\"value\":6.0,\"unit\":\"m2\",\"symbol\":\"A\"},{\"value\":20.0,\"unit\":\"kN/m3\",\"symbol\":\"gamma_mt\"},{\"value\":1.0,\"unit\":\"m\",\"symbol\":\"d\"},{\"value\":-60.0,\"unit\":\"kN*m\",\"symbol\":\"M_x\"},{\"value\":2.0,\"unit\":\"m3\",\"symbol\":\"W_x\"},{\"value\":-45.0,\"unit\":\"kN*m\",\"symbol\":\"M_y\"},{\"value\":3.0,\"unit\":\"m3\",\"symbol\":\"W_y\"}],\"result\":{\"value\":75.0,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.29, formula (5.15)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"kind\":\"engineer_formula\",\"step_id\":\"p_corner_mp\",\"expression\":\"p_{mp}=p+s_x M_{x,base}/W_x+s_y M_{y,base}/W_y\",\"substitutions\":[{\"value\":120.0,\"unit\":\"kPa\",\"symbol\":\"p\"},{\"value\":60.0,\"unit\":\"kN*m\",\"symbol\":\"Mx_base\"},{\"value\":2.0,\"unit\":\"m3\",\"symbol\":\"Wx\"},{\"value\":-45.0,\"unit\":\"kN*m\",\"symbol\":\"My_base\"},{\"value\":3.0,\"unit\":\"m3\",\"symbol\":\"Wy\"},{\"value\":-1.0,\"unit\":\"1\",\"symbol\":\"sign_x_mp\"},{\"value\":1.0,\"unit\":\"1\",\"symbol\":\"sign_y_mp\"},{\"value\":75.0,\"unit\":\"kPa\",\"symbol\":\"corner_component_mp\"}],\"result\":{\"value\":75.0,\"unit\":\"kPa\"},\"source\":{\"engineer\":\"Аким\",\"rationale\":\"Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08.\"}},{\"step_id\":\"corner_component_mm\",\"expression\":\"P_{\\\\max}=\\\\frac{N}{A}+\\\\gamma_{mt}d+\\\\frac{M_x}{W_x}+\\\\frac{M_y}{W_y}\",\"substitutions\":[{\"value\":600.0,\"unit\":\"kN\",\"symbol\":\"N\"},{\"value\":6.0,\"unit\":\"m2\",\"symbol\":\"A\"},{\"value\":20.0,\"unit\":\"kN/m3\",\"symbol\":\"gamma_mt\"},{\"value\":1.0,\"unit\":\"m\",\"symbol\":\"d\"},{\"value\":-60.0,\"unit\":\"kN*m\",\"symbol\":\"M_x\"},{\"value\":2.0,\"unit\":\"m3\",\"symbol\":\"W_x\"},{\"value\":45.0,\"unit\":\"kN*m\",\"symbol\":\"M_y\"},{\"value\":3.0,\"unit\":\"m3\",\"symbol\":\"W_y\"}],\"result\":{\"value\":105.0,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.29, formula (5.15)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"kind\":\"engineer_formula\",\"step_id\":\"p_corner_mm\",\"expression\":\"p_{mm}=p+s_x M_{x,base}/W_x+s_y M_{y,base}/W_y\",\"substitutions\":[{\"value\":120.0,\"unit\":\"kPa\",\"symbol\":\"p\"},{\"value\":60.0,\"unit\":\"kN*m\",\"symbol\":\"Mx_base\"},{\"value\":2.0,\"unit\":\"m3\",\"symbol\":\"Wx\"},{\"value\":-45.0,\"unit\":\"kN*m\",\"symbol\":\"My_base\"},{\"value\":3.0,\"unit\":\"m3\",\"symbol\":\"Wy\"},{\"value\":-1.0,\"unit\":\"1\",\"symbol\":\"sign_x_mm\"},{\"value\":-1.0,\"unit\":\"1\",\"symbol\":\"sign_y_mm\"},{\"value\":105.0,\"unit\":\"kPa\",\"symbol\":\"corner_component_mm\"}],\"result\":{\"value\":105.0,\"unit\":\"kPa\"},\"source\":{\"engineer\":\"Аким\",\"rationale\":\"Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08.\"}},{\"kind\":\"engineer_formula\",\"step_id\":\"p_corner_min\",\"expression\":\"p_{corner,min}=\\\\min(p_{++},p_{+-},p_{-+},p_{--})\",\"substitutions\":[{\"value\":135.0,\"unit\":\"kPa\",\"symbol\":\"p_corner_pp\"},{\"value\":165.0,\"unit\":\"kPa\",\"symbol\":\"p_corner_pm\"},{\"value\":75.0,\"unit\":\"kPa\",\"symbol\":\"p_corner_mp\"},{\"value\":105.0,\"unit\":\"kPa\",\"symbol\":\"p_corner_mm\"}],\"result\":{\"value\":75.0,\"unit\":\"kPa\"},\"source\":{\"engineer\":\"Аким\",\"rationale\":\"Полный контакт прямоугольной подошвы: минимум четырёх подписанных угловых давлений неотрицателен; решение инженера 2026-11-08.\"}},{\"kind\":\"engineer_formula\",\"step_id\":\"p_corner_max\",\"expression\":\"p_{corner,max}=\\\\max(p_{++},p_{+-},p_{-+},p_{--})\",\"substitutions\":[{\"value\":135.0,\"unit\":\"kPa\",\"symbol\":\"p_corner_pp\"},{\"value\":165.0,\"unit\":\"kPa\",\"symbol\":\"p_corner_pm\"},{\"value\":75.0,\"unit\":\"kPa\",\"symbol\":\"p_corner_mp\"},{\"value\":105.0,\"unit\":\"kPa\",\"symbol\":\"p_corner_mm\"}],\"result\":{\"value\":165.0,\"unit\":\"kPa\"},\"source\":{\"engineer\":\"Аким\",\"rationale\":\"Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08.\"}},{\"step_id\":\"edge_limit_multiplier\",\"expression\":\"edge_limit_multiplier\",\"substitutions\":[],\"result\":{\"value\":1.2,\"unit\":\"1\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.26\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"table\"},{\"step_id\":\"edge_limit\",\"expression\":\"p_{edge,lim}=\\\\lambda_e R\",\"substitutions\":[{\"value\":1.2,\"unit\":\"1\",\"symbol\":\"edge_limit_multiplier\"},{\"value\":152.02,\"unit\":\"kPa\",\"symbol\":\"R\"}],\"result\":{\"value\":182.424,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.26\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"step_id\":\"corner_limit_multiplier\",\"expression\":\"corner_limit_multiplier\",\"substitutions\":[],\"result\":{\"value\":1.5,\"unit\":\"1\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.26\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"table\"},{\"step_id\":\"corner_limit\",\"expression\":\"p_{corner,lim}=\\\\lambda_c R\",\"substitutions\":[{\"value\":1.5,\"unit\":\"1\",\"symbol\":\"corner_limit_multiplier\"},{\"value\":152.02,\"unit\":\"kPa\",\"symbol\":\"R\"}],\"result\":{\"value\":228.03000000000003,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.26\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"step_id\":\"p_le_R\",\"expression\":\"p \\\\le R\",\"substitutions\":[{\"value\":120.0,\"unit\":\"kPa\",\"symbol\":\"p\"},{\"value\":152.02,\"unit\":\"kPa\",\"symbol\":\"R\"}],\"result\":{\"value\":120.0,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"check\",\"operator\":\"le\",\"right\":{\"value\":152.02,\"unit\":\"kPa\"},\"passed\":true},{\"step_id\":\"p_x_max_le_limit\",\"expression\":\"p_x_max \\\\le edge_limit\",\"substitutions\":[{\"value\":150.0,\"unit\":\"kPa\",\"symbol\":\"p_x_max\"},{\"value\":182.424,\"unit\":\"kPa\",\"symbol\":\"edge_limit\"}],\"result\":{\"value\":150.0,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.26\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"check\",\"operator\":\"le\",\"right\":{\"value\":182.424,\"unit\":\"kPa\"},\"passed\":true},{\"step_id\":\"p_y_max_le_limit\",\"expression\":\"p_y_max \\\\le edge_limit\",\"substitutions\":[{\"value\":135.0,\"unit\":\"kPa\",\"symbol\":\"p_y_max\"},{\"value\":182.424,\"unit\":\"kPa\",\"symbol\":\"edge_limit\"}],\"result\":{\"value\":135.0,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.26\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"check\",\"operator\":\"le\",\"right\":{\"value\":182.424,\"unit\":\"kPa\"},\"passed\":true},{\"step_id\":\"p_corner_max_le_limit\",\"expression\":\"p_corner_max \\\\le corner_limit\",\"substitutions\":[{\"value\":165.0,\"unit\":\"kPa\",\"symbol\":\"p_corner_max\"},{\"value\":228.03000000000003,\"unit\":\"kPa\",\"symbol\":\"corner_limit\"}],\"result\":{\"value\":165.0,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.26\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"check\",\"operator\":\"le\",\"right\":{\"value\":228.03000000000003,\"unit\":\"kPa\"},\"passed\":true}],\"unverified_step_count\":30,\"result_id\":\"77777777-7777-4777-8777-777777777777\",\"parameter_source\":{\"kind\":\"interim\",\"data_sha256\":\"faaa0724af57ca6c8066f558c4e75c2785d099b34cbfb07c4a85892fdc3b68fe\",\"profile\":\"strict\"}}"

export const LOADS_FAIL_ID = '88888888-8888-4888-8888-888888888888'

export const loadsFailInputs = {
  "b": {
    "value": 2,
    "unit": "m"
  },
  "d_1": {
    "value": 1,
    "unit": "m"
  },
  "d_b": {
    "value": 0,
    "unit": "m"
  },
  "gamma_II": {
    "value": 20,
    "unit": "kN/m3"
  },
  "gamma_II_prime": {
    "value": 20,
    "unit": "kN/m3"
  },
  "c_II": {
    "value": 10,
    "unit": "kPa"
  },
  "phi_II": {
    "value": 20,
    "unit": "deg"
  },
  "l": {
    "value": 3,
    "unit": "m"
  },
  "h": {
    "value": 1,
    "unit": "m"
  },
  "d": {
    "value": 1,
    "unit": "m"
  },
  "N": {
    "value": 900,
    "unit": "kN"
  },
  "Mx": {
    "value": 0,
    "unit": "kN*m"
  },
  "My": {
    "value": 0,
    "unit": "kN*m"
  },
  "Qx": {
    "value": 0,
    "unit": "kN"
  },
  "Qy": {
    "value": 0,
    "unit": "kN"
  }
} satisfies CalculationRequest['inputs']

export const loadsFailEnvelope = {
  "engine_version": "0.1.0",
  "input_hash": "14af66e093c1ab9096f1ef6952391443716d0c3ec9b2774dcce1b917d9379396", // pragma: allowlist secret
  "outputs": [
    {
      "value": 152.02,
      "unit": "kPa",
      "quantity": "R",
      "rounding_rule": {
        "decimals": 2,
        "mode": "half_up"
      },
      "rounding_source": {
        "engineer": "Аким",
        "rationale": "Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются."
      }
    },
    {
      "value": 170.0,
      "unit": "kPa",
      "quantity": "p",
      "rounding_rule": {
        "decimals": 2,
        "mode": "half_up"
      },
      "rounding_source": {
        "engineer": "Аким",
        "rationale": "Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются."
      }
    },
    {
      "value": 170.0,
      "unit": "kPa",
      "quantity": "p_x_min",
      "rounding_rule": {
        "decimals": 2,
        "mode": "half_up"
      },
      "rounding_source": {
        "engineer": "Аким",
        "rationale": "Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются."
      }
    },
    {
      "value": 170.0,
      "unit": "kPa",
      "quantity": "p_x_max",
      "rounding_rule": {
        "decimals": 2,
        "mode": "half_up"
      },
      "rounding_source": {
        "engineer": "Аким",
        "rationale": "Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются."
      }
    },
    {
      "value": 170.0,
      "unit": "kPa",
      "quantity": "p_y_min",
      "rounding_rule": {
        "decimals": 2,
        "mode": "half_up"
      },
      "rounding_source": {
        "engineer": "Аким",
        "rationale": "Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются."
      }
    },
    {
      "value": 170.0,
      "unit": "kPa",
      "quantity": "p_y_max",
      "rounding_rule": {
        "decimals": 2,
        "mode": "half_up"
      },
      "rounding_source": {
        "engineer": "Аким",
        "rationale": "Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются."
      }
    },
    {
      "value": 170.0,
      "unit": "kPa",
      "quantity": "p_corner_pp",
      "rounding_rule": {
        "decimals": 2,
        "mode": "half_up"
      },
      "rounding_source": {
        "engineer": "Аким",
        "rationale": "Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются."
      }
    },
    {
      "value": 170.0,
      "unit": "kPa",
      "quantity": "p_corner_pm",
      "rounding_rule": {
        "decimals": 2,
        "mode": "half_up"
      },
      "rounding_source": {
        "engineer": "Аким",
        "rationale": "Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются."
      }
    },
    {
      "value": 170.0,
      "unit": "kPa",
      "quantity": "p_corner_mp",
      "rounding_rule": {
        "decimals": 2,
        "mode": "half_up"
      },
      "rounding_source": {
        "engineer": "Аким",
        "rationale": "Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются."
      }
    },
    {
      "value": 170.0,
      "unit": "kPa",
      "quantity": "p_corner_mm",
      "rounding_rule": {
        "decimals": 2,
        "mode": "half_up"
      },
      "rounding_source": {
        "engineer": "Аким",
        "rationale": "Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются."
      }
    }
  ],
  "norm_refs": [
    {
      "document": "СП 22.13330.2016",
      "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
      "clause": "5.6.7, таблица 5.4",
      "status": "unverified",
      "provenance": "machine-extracted"
    },
    {
      "document": "СП 22.13330.2016",
      "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
      "clause": "5.6.7, экспликация k",
      "status": "unverified",
      "provenance": "machine-extracted"
    },
    {
      "document": "СП 22.13330.2016",
      "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
      "clause": "5.6.7, таблица 5.5",
      "status": "unverified",
      "provenance": "machine-extracted"
    },
    {
      "document": "СП 22.13330.2016",
      "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
      "clause": "5.6.7, экспликация k_z",
      "status": "unverified",
      "provenance": "machine-extracted"
    },
    {
      "document": "СП 22.13330.2016",
      "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
      "clause": "5.6.7, формула (5.7)",
      "status": "unverified",
      "provenance": "machine-extracted"
    },
    {
      "document": "СП 22.13330.2016",
      "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
      "clause": "5.6.28, explanation of formula (5.11)",
      "status": "unverified",
      "provenance": "machine-extracted"
    },
    {
      "document": "СП 22.13330.2016",
      "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
      "clause": "5.6.28, formula (5.11)",
      "status": "unverified",
      "provenance": "machine-extracted"
    },
    {
      "document": "СП 22.13330.2016",
      "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
      "clause": "5.6.28, applicability of formula (5.11)",
      "status": "unverified",
      "provenance": "machine-extracted"
    },
    {
      "document": "СП 22.13330.2016",
      "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
      "clause": "5.6.27, figure 5.1",
      "status": "unverified",
      "provenance": "machine-extracted"
    },
    {
      "document": "СП 22.13330.2016",
      "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
      "clause": "5.6.29, formula (5.15)",
      "status": "unverified",
      "provenance": "machine-extracted"
    },
    {
      "document": "СП 22.13330.2016",
      "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
      "clause": "5.6.26",
      "status": "unverified",
      "provenance": "machine-extracted"
    },
    {
      "document": "СП 22.13330.2016",
      "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
      "clause": "5.6.7",
      "status": "unverified",
      "provenance": "machine-extracted"
    }
  ],
  "engineer_rules": [
    {
      "engineer": "Аким",
      "rationale": "Геометрия прямоугольной подошвы: A=b*l, Wx=l*b²/6, Wy=b*l²/6; инженерный контракт 2026-11-08."
    },
    {
      "engineer": "Аким",
      "rationale": "Подписанный перенос нагрузок к подошве M_base=M+Q*h; оси x=b и y=l; инженерный контракт 2026-11-08."
    },
    {
      "engineer": "Аким",
      "rationale": "Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08."
    },
    {
      "engineer": "Аким",
      "rationale": "Полный контакт прямоугольной подошвы: минимум четырёх подписанных угловых давлений неотрицателен; решение инженера 2026-11-08."
    },
    {
      "engineer": "Аким",
      "rationale": "Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются."
    }
  ],
  "verdict": "fail",
  "verdict_reason": {
    "kind": "check",
    "step_id": "p_le_R"
  },
  "warnings": [],
  "trace": [
    {
      "step_id": "gamma_c1",
      "expression": "\\gamma_{c1}",
      "substitutions": [],
      "result": {
        "value": 1.1,
        "unit": "1"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.7, таблица 5.4",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "table"
    },
    {
      "step_id": "gamma_c2",
      "expression": "\\gamma_{c2}",
      "substitutions": [],
      "result": {
        "value": 1.0,
        "unit": "1"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.7, таблица 5.4",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "table"
    },
    {
      "step_id": "k",
      "expression": "k",
      "substitutions": [],
      "result": {
        "value": 1.0,
        "unit": "1"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.7, экспликация k",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "table"
    },
    {
      "step_id": "M_gamma",
      "expression": "M_{\\gamma} = M_{\\gamma}\\left(\\varphi_{II}\\right)",
      "substitutions": [
        {
          "value": 20.0,
          "unit": "deg",
          "symbol": "phi_II"
        }
      ],
      "result": {
        "value": 0.51,
        "unit": "1"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.7, таблица 5.5",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "table"
    },
    {
      "step_id": "M_q",
      "expression": "M_{q} = M_{q}\\left(\\varphi_{II}\\right)",
      "substitutions": [
        {
          "value": 20.0,
          "unit": "deg",
          "symbol": "phi_II"
        }
      ],
      "result": {
        "value": 3.06,
        "unit": "1"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.7, таблица 5.5",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "table"
    },
    {
      "step_id": "M_c",
      "expression": "M_{c} = M_{c}\\left(\\varphi_{II}\\right)",
      "substitutions": [
        {
          "value": 20.0,
          "unit": "deg",
          "symbol": "phi_II"
        }
      ],
      "result": {
        "value": 5.66,
        "unit": "1"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.7, таблица 5.5",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "table"
    },
    {
      "step_id": "k_z",
      "expression": "k_{z}=1",
      "substitutions": [],
      "result": {
        "value": 1.0,
        "unit": "1"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.7, экспликация k_z",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "step_id": "R",
      "expression": "R=\\frac{\\gamma_{c1}\\gamma_{c2}}{k}\\left[M_{\\gamma}k_{z}b\\gamma_{II}+M_{q}d_{1}\\gamma'_{II}+(M_{q}-1)d_{b}\\gamma'_{II}+M_{c}c_{II}\\right]",
      "substitutions": [
        {
          "value": 1.1,
          "unit": "1",
          "symbol": "gamma_c1"
        },
        {
          "value": 1.0,
          "unit": "1",
          "symbol": "gamma_c2"
        },
        {
          "value": 1.0,
          "unit": "1",
          "symbol": "k"
        },
        {
          "value": 0.51,
          "unit": "1",
          "symbol": "M_gamma"
        },
        {
          "value": 1.0,
          "unit": "1",
          "symbol": "k_z"
        },
        {
          "value": 2.0,
          "unit": "m",
          "symbol": "b"
        },
        {
          "value": 20.0,
          "unit": "kN/m3",
          "symbol": "gamma_II"
        },
        {
          "value": 3.06,
          "unit": "1",
          "symbol": "M_q"
        },
        {
          "value": 1.0,
          "unit": "m",
          "symbol": "d_1"
        },
        {
          "value": 20.0,
          "unit": "kN/m3",
          "symbol": "gamma_II_prime"
        },
        {
          "value": 0.0,
          "unit": "m",
          "symbol": "d_b"
        },
        {
          "value": 5.66,
          "unit": "1",
          "symbol": "M_c"
        },
        {
          "value": 10.0,
          "unit": "kPa",
          "symbol": "c_II"
        }
      ],
      "result": {
        "value": 152.02,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.7, формула (5.7)",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "kind": "engineer_formula",
      "step_id": "A",
      "expression": "A=b l",
      "substitutions": [
        {
          "value": 2.0,
          "unit": "m",
          "symbol": "b"
        },
        {
          "value": 3.0,
          "unit": "m",
          "symbol": "l"
        }
      ],
      "result": {
        "value": 6.0,
        "unit": "m2"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Геометрия прямоугольной подошвы: A=b*l, Wx=l*b²/6, Wy=b*l²/6; инженерный контракт 2026-11-08."
      }
    },
    {
      "kind": "engineer_formula",
      "step_id": "Wx",
      "expression": "W_x=l b^2/6",
      "substitutions": [
        {
          "value": 2.0,
          "unit": "m",
          "symbol": "b"
        },
        {
          "value": 3.0,
          "unit": "m",
          "symbol": "l"
        }
      ],
      "result": {
        "value": 2.0,
        "unit": "m3"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Геометрия прямоугольной подошвы: A=b*l, Wx=l*b²/6, Wy=b*l²/6; инженерный контракт 2026-11-08."
      }
    },
    {
      "kind": "engineer_formula",
      "step_id": "Wy",
      "expression": "W_y=b l^2/6",
      "substitutions": [
        {
          "value": 2.0,
          "unit": "m",
          "symbol": "b"
        },
        {
          "value": 3.0,
          "unit": "m",
          "symbol": "l"
        }
      ],
      "result": {
        "value": 3.0,
        "unit": "m3"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Геометрия прямоугольной подошвы: A=b*l, Wx=l*b²/6, Wy=b*l²/6; инженерный контракт 2026-11-08."
      }
    },
    {
      "kind": "engineer_formula",
      "step_id": "Mx_base",
      "expression": "M_{x,base}=M_x+Q_x h",
      "substitutions": [
        {
          "value": 0.0,
          "unit": "kN*m",
          "symbol": "Mx"
        },
        {
          "value": 0.0,
          "unit": "kN",
          "symbol": "Qx"
        },
        {
          "value": 1.0,
          "unit": "m",
          "symbol": "h"
        }
      ],
      "result": {
        "value": 0.0,
        "unit": "kN*m"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Подписанный перенос нагрузок к подошве M_base=M+Q*h; оси x=b и y=l; инженерный контракт 2026-11-08."
      }
    },
    {
      "kind": "engineer_formula",
      "step_id": "My_base",
      "expression": "M_{y,base}=M_y+Q_y h",
      "substitutions": [
        {
          "value": 0.0,
          "unit": "kN*m",
          "symbol": "My"
        },
        {
          "value": 0.0,
          "unit": "kN",
          "symbol": "Qy"
        },
        {
          "value": 1.0,
          "unit": "m",
          "symbol": "h"
        }
      ],
      "result": {
        "value": 0.0,
        "unit": "kN*m"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Подписанный перенос нагрузок к подошве M_base=M+Q*h; оси x=b и y=l; инженерный контракт 2026-11-08."
      }
    },
    {
      "step_id": "gamma_mt",
      "expression": "\\gamma_{mt}",
      "substitutions": [],
      "result": {
        "value": 20.0,
        "unit": "kN/m3"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.28, explanation of formula (5.11)",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "table"
    },
    {
      "step_id": "p",
      "expression": "p_{+}=\\frac{N}{A}+\\gamma_{mt}d+\\frac{M}{W}",
      "substitutions": [
        {
          "value": 900.0,
          "unit": "kN",
          "symbol": "N"
        },
        {
          "value": 6.0,
          "unit": "m2",
          "symbol": "A"
        },
        {
          "value": 20.0,
          "unit": "kN/m3",
          "symbol": "gamma_mt"
        },
        {
          "value": 1.0,
          "unit": "m",
          "symbol": "d"
        },
        {
          "value": 0.0,
          "unit": "kN*m",
          "symbol": "M"
        },
        {
          "value": 2.0,
          "unit": "m3",
          "symbol": "W"
        }
      ],
      "result": {
        "value": 170.0,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.28, formula (5.11)",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "kind": "engineer_formula",
      "step_id": "V",
      "expression": "V=N+\\gamma_{mt} d A",
      "substitutions": [
        {
          "value": 900.0,
          "unit": "kN",
          "symbol": "N"
        },
        {
          "value": 20.0,
          "unit": "kN/m3",
          "symbol": "gamma_mt"
        },
        {
          "value": 1.0,
          "unit": "m",
          "symbol": "d"
        },
        {
          "value": 6.0,
          "unit": "m2",
          "symbol": "A"
        }
      ],
      "result": {
        "value": 1020.0,
        "unit": "kN"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08."
      }
    },
    {
      "step_id": "p_x_min",
      "expression": "p_{-}=\\frac{N}{A}+\\gamma_{mt}d-\\frac{M}{W}",
      "substitutions": [
        {
          "value": 900.0,
          "unit": "kN",
          "symbol": "N"
        },
        {
          "value": 6.0,
          "unit": "m2",
          "symbol": "A"
        },
        {
          "value": 20.0,
          "unit": "kN/m3",
          "symbol": "gamma_mt"
        },
        {
          "value": 1.0,
          "unit": "m",
          "symbol": "d"
        },
        {
          "value": 0.0,
          "unit": "kN*m",
          "symbol": "M"
        },
        {
          "value": 2.0,
          "unit": "m3",
          "symbol": "W"
        }
      ],
      "result": {
        "value": 170.0,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.28, formula (5.11)",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "step_id": "p_x_max",
      "expression": "p_{+}=\\frac{N}{A}+\\gamma_{mt}d+\\frac{M}{W}",
      "substitutions": [
        {
          "value": 900.0,
          "unit": "kN",
          "symbol": "N"
        },
        {
          "value": 6.0,
          "unit": "m2",
          "symbol": "A"
        },
        {
          "value": 20.0,
          "unit": "kN/m3",
          "symbol": "gamma_mt"
        },
        {
          "value": 1.0,
          "unit": "m",
          "symbol": "d"
        },
        {
          "value": 0.0,
          "unit": "kN*m",
          "symbol": "M"
        },
        {
          "value": 2.0,
          "unit": "m3",
          "symbol": "W"
        }
      ],
      "result": {
        "value": 170.0,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.28, formula (5.11)",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "kind": "engineer_formula",
      "step_id": "e_x",
      "expression": "e_x=|M_{x,base}|/V",
      "substitutions": [
        {
          "value": 0.0,
          "unit": "kN*m",
          "symbol": "Mx_base"
        },
        {
          "value": 1020.0,
          "unit": "kN",
          "symbol": "V"
        }
      ],
      "result": {
        "value": 0.0,
        "unit": "m"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08."
      }
    },
    {
      "step_id": "relative_eccentricity_x",
      "expression": "e/l\\leq1/6",
      "substitutions": [
        {
          "value": 0.0,
          "unit": "1",
          "symbol": "e/L"
        },
        {
          "value": 1.0,
          "unit": "1",
          "symbol": "numerator"
        },
        {
          "value": 6.0,
          "unit": "1",
          "symbol": "denominator"
        }
      ],
      "result": {
        "value": 1.0,
        "unit": "1"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.28, applicability of formula (5.11)",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "step_id": "pressure_diagram_x",
      "expression": "e<l/6",
      "substitutions": [
        {
          "value": 0.0,
          "unit": "m",
          "symbol": "e"
        },
        {
          "value": 2.0,
          "unit": "m",
          "symbol": "l"
        }
      ],
      "result": {
        "value": 0.0,
        "unit": "m"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.27, figure 5.1",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "step_id": "p_y_min",
      "expression": "p_{-}=\\frac{N}{A}+\\gamma_{mt}d-\\frac{M}{W}",
      "substitutions": [
        {
          "value": 900.0,
          "unit": "kN",
          "symbol": "N"
        },
        {
          "value": 6.0,
          "unit": "m2",
          "symbol": "A"
        },
        {
          "value": 20.0,
          "unit": "kN/m3",
          "symbol": "gamma_mt"
        },
        {
          "value": 1.0,
          "unit": "m",
          "symbol": "d"
        },
        {
          "value": 0.0,
          "unit": "kN*m",
          "symbol": "M"
        },
        {
          "value": 3.0,
          "unit": "m3",
          "symbol": "W"
        }
      ],
      "result": {
        "value": 170.0,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.28, formula (5.11)",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "step_id": "p_y_max",
      "expression": "p_{+}=\\frac{N}{A}+\\gamma_{mt}d+\\frac{M}{W}",
      "substitutions": [
        {
          "value": 900.0,
          "unit": "kN",
          "symbol": "N"
        },
        {
          "value": 6.0,
          "unit": "m2",
          "symbol": "A"
        },
        {
          "value": 20.0,
          "unit": "kN/m3",
          "symbol": "gamma_mt"
        },
        {
          "value": 1.0,
          "unit": "m",
          "symbol": "d"
        },
        {
          "value": 0.0,
          "unit": "kN*m",
          "symbol": "M"
        },
        {
          "value": 3.0,
          "unit": "m3",
          "symbol": "W"
        }
      ],
      "result": {
        "value": 170.0,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.28, formula (5.11)",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "kind": "engineer_formula",
      "step_id": "e_y",
      "expression": "e_y=|M_{y,base}|/V",
      "substitutions": [
        {
          "value": 0.0,
          "unit": "kN*m",
          "symbol": "My_base"
        },
        {
          "value": 1020.0,
          "unit": "kN",
          "symbol": "V"
        }
      ],
      "result": {
        "value": 0.0,
        "unit": "m"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08."
      }
    },
    {
      "step_id": "relative_eccentricity_y",
      "expression": "e/l\\leq1/6",
      "substitutions": [
        {
          "value": 0.0,
          "unit": "1",
          "symbol": "e/L"
        },
        {
          "value": 1.0,
          "unit": "1",
          "symbol": "numerator"
        },
        {
          "value": 6.0,
          "unit": "1",
          "symbol": "denominator"
        }
      ],
      "result": {
        "value": 1.0,
        "unit": "1"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.28, applicability of formula (5.11)",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "step_id": "pressure_diagram_y",
      "expression": "e<l/6",
      "substitutions": [
        {
          "value": 0.0,
          "unit": "m",
          "symbol": "e"
        },
        {
          "value": 3.0,
          "unit": "m",
          "symbol": "l"
        }
      ],
      "result": {
        "value": 0.0,
        "unit": "m"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.27, figure 5.1",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "step_id": "corner_component_pp",
      "expression": "P_{\\max}=\\frac{N}{A}+\\gamma_{mt}d+\\frac{M_x}{W_x}+\\frac{M_y}{W_y}",
      "substitutions": [
        {
          "value": 900.0,
          "unit": "kN",
          "symbol": "N"
        },
        {
          "value": 6.0,
          "unit": "m2",
          "symbol": "A"
        },
        {
          "value": 20.0,
          "unit": "kN/m3",
          "symbol": "gamma_mt"
        },
        {
          "value": 1.0,
          "unit": "m",
          "symbol": "d"
        },
        {
          "value": 0.0,
          "unit": "kN*m",
          "symbol": "M_x"
        },
        {
          "value": 2.0,
          "unit": "m3",
          "symbol": "W_x"
        },
        {
          "value": 0.0,
          "unit": "kN*m",
          "symbol": "M_y"
        },
        {
          "value": 3.0,
          "unit": "m3",
          "symbol": "W_y"
        }
      ],
      "result": {
        "value": 170.0,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.29, formula (5.15)",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "kind": "engineer_formula",
      "step_id": "p_corner_pp",
      "expression": "p_{pp}=p+s_x M_{x,base}/W_x+s_y M_{y,base}/W_y",
      "substitutions": [
        {
          "value": 170.0,
          "unit": "kPa",
          "symbol": "p"
        },
        {
          "value": 0.0,
          "unit": "kN*m",
          "symbol": "Mx_base"
        },
        {
          "value": 2.0,
          "unit": "m3",
          "symbol": "Wx"
        },
        {
          "value": 0.0,
          "unit": "kN*m",
          "symbol": "My_base"
        },
        {
          "value": 3.0,
          "unit": "m3",
          "symbol": "Wy"
        },
        {
          "value": 1.0,
          "unit": "1",
          "symbol": "sign_x_pp"
        },
        {
          "value": 1.0,
          "unit": "1",
          "symbol": "sign_y_pp"
        },
        {
          "value": 170.0,
          "unit": "kPa",
          "symbol": "corner_component_pp"
        }
      ],
      "result": {
        "value": 170.0,
        "unit": "kPa"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08."
      }
    },
    {
      "step_id": "corner_component_pm",
      "expression": "P_{\\max}=\\frac{N}{A}+\\gamma_{mt}d+\\frac{M_x}{W_x}+\\frac{M_y}{W_y}",
      "substitutions": [
        {
          "value": 900.0,
          "unit": "kN",
          "symbol": "N"
        },
        {
          "value": 6.0,
          "unit": "m2",
          "symbol": "A"
        },
        {
          "value": 20.0,
          "unit": "kN/m3",
          "symbol": "gamma_mt"
        },
        {
          "value": 1.0,
          "unit": "m",
          "symbol": "d"
        },
        {
          "value": 0.0,
          "unit": "kN*m",
          "symbol": "M_x"
        },
        {
          "value": 2.0,
          "unit": "m3",
          "symbol": "W_x"
        },
        {
          "value": -0.0,
          "unit": "kN*m",
          "symbol": "M_y"
        },
        {
          "value": 3.0,
          "unit": "m3",
          "symbol": "W_y"
        }
      ],
      "result": {
        "value": 170.0,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.29, formula (5.15)",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "kind": "engineer_formula",
      "step_id": "p_corner_pm",
      "expression": "p_{pm}=p+s_x M_{x,base}/W_x+s_y M_{y,base}/W_y",
      "substitutions": [
        {
          "value": 170.0,
          "unit": "kPa",
          "symbol": "p"
        },
        {
          "value": 0.0,
          "unit": "kN*m",
          "symbol": "Mx_base"
        },
        {
          "value": 2.0,
          "unit": "m3",
          "symbol": "Wx"
        },
        {
          "value": 0.0,
          "unit": "kN*m",
          "symbol": "My_base"
        },
        {
          "value": 3.0,
          "unit": "m3",
          "symbol": "Wy"
        },
        {
          "value": 1.0,
          "unit": "1",
          "symbol": "sign_x_pm"
        },
        {
          "value": -1.0,
          "unit": "1",
          "symbol": "sign_y_pm"
        },
        {
          "value": 170.0,
          "unit": "kPa",
          "symbol": "corner_component_pm"
        }
      ],
      "result": {
        "value": 170.0,
        "unit": "kPa"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08."
      }
    },
    {
      "step_id": "corner_component_mp",
      "expression": "P_{\\max}=\\frac{N}{A}+\\gamma_{mt}d+\\frac{M_x}{W_x}+\\frac{M_y}{W_y}",
      "substitutions": [
        {
          "value": 900.0,
          "unit": "kN",
          "symbol": "N"
        },
        {
          "value": 6.0,
          "unit": "m2",
          "symbol": "A"
        },
        {
          "value": 20.0,
          "unit": "kN/m3",
          "symbol": "gamma_mt"
        },
        {
          "value": 1.0,
          "unit": "m",
          "symbol": "d"
        },
        {
          "value": -0.0,
          "unit": "kN*m",
          "symbol": "M_x"
        },
        {
          "value": 2.0,
          "unit": "m3",
          "symbol": "W_x"
        },
        {
          "value": 0.0,
          "unit": "kN*m",
          "symbol": "M_y"
        },
        {
          "value": 3.0,
          "unit": "m3",
          "symbol": "W_y"
        }
      ],
      "result": {
        "value": 170.0,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.29, formula (5.15)",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "kind": "engineer_formula",
      "step_id": "p_corner_mp",
      "expression": "p_{mp}=p+s_x M_{x,base}/W_x+s_y M_{y,base}/W_y",
      "substitutions": [
        {
          "value": 170.0,
          "unit": "kPa",
          "symbol": "p"
        },
        {
          "value": 0.0,
          "unit": "kN*m",
          "symbol": "Mx_base"
        },
        {
          "value": 2.0,
          "unit": "m3",
          "symbol": "Wx"
        },
        {
          "value": 0.0,
          "unit": "kN*m",
          "symbol": "My_base"
        },
        {
          "value": 3.0,
          "unit": "m3",
          "symbol": "Wy"
        },
        {
          "value": -1.0,
          "unit": "1",
          "symbol": "sign_x_mp"
        },
        {
          "value": 1.0,
          "unit": "1",
          "symbol": "sign_y_mp"
        },
        {
          "value": 170.0,
          "unit": "kPa",
          "symbol": "corner_component_mp"
        }
      ],
      "result": {
        "value": 170.0,
        "unit": "kPa"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08."
      }
    },
    {
      "step_id": "corner_component_mm",
      "expression": "P_{\\max}=\\frac{N}{A}+\\gamma_{mt}d+\\frac{M_x}{W_x}+\\frac{M_y}{W_y}",
      "substitutions": [
        {
          "value": 900.0,
          "unit": "kN",
          "symbol": "N"
        },
        {
          "value": 6.0,
          "unit": "m2",
          "symbol": "A"
        },
        {
          "value": 20.0,
          "unit": "kN/m3",
          "symbol": "gamma_mt"
        },
        {
          "value": 1.0,
          "unit": "m",
          "symbol": "d"
        },
        {
          "value": -0.0,
          "unit": "kN*m",
          "symbol": "M_x"
        },
        {
          "value": 2.0,
          "unit": "m3",
          "symbol": "W_x"
        },
        {
          "value": -0.0,
          "unit": "kN*m",
          "symbol": "M_y"
        },
        {
          "value": 3.0,
          "unit": "m3",
          "symbol": "W_y"
        }
      ],
      "result": {
        "value": 170.0,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.29, formula (5.15)",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "kind": "engineer_formula",
      "step_id": "p_corner_mm",
      "expression": "p_{mm}=p+s_x M_{x,base}/W_x+s_y M_{y,base}/W_y",
      "substitutions": [
        {
          "value": 170.0,
          "unit": "kPa",
          "symbol": "p"
        },
        {
          "value": 0.0,
          "unit": "kN*m",
          "symbol": "Mx_base"
        },
        {
          "value": 2.0,
          "unit": "m3",
          "symbol": "Wx"
        },
        {
          "value": 0.0,
          "unit": "kN*m",
          "symbol": "My_base"
        },
        {
          "value": 3.0,
          "unit": "m3",
          "symbol": "Wy"
        },
        {
          "value": -1.0,
          "unit": "1",
          "symbol": "sign_x_mm"
        },
        {
          "value": -1.0,
          "unit": "1",
          "symbol": "sign_y_mm"
        },
        {
          "value": 170.0,
          "unit": "kPa",
          "symbol": "corner_component_mm"
        }
      ],
      "result": {
        "value": 170.0,
        "unit": "kPa"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08."
      }
    },
    {
      "kind": "engineer_formula",
      "step_id": "p_corner_min",
      "expression": "p_{corner,min}=\\min(p_{++},p_{+-},p_{-+},p_{--})",
      "substitutions": [
        {
          "value": 170.0,
          "unit": "kPa",
          "symbol": "p_corner_pp"
        },
        {
          "value": 170.0,
          "unit": "kPa",
          "symbol": "p_corner_pm"
        },
        {
          "value": 170.0,
          "unit": "kPa",
          "symbol": "p_corner_mp"
        },
        {
          "value": 170.0,
          "unit": "kPa",
          "symbol": "p_corner_mm"
        }
      ],
      "result": {
        "value": 170.0,
        "unit": "kPa"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Полный контакт прямоугольной подошвы: минимум четырёх подписанных угловых давлений неотрицателен; решение инженера 2026-11-08."
      }
    },
    {
      "kind": "engineer_formula",
      "step_id": "p_corner_max",
      "expression": "p_{corner,max}=\\max(p_{++},p_{+-},p_{-+},p_{--})",
      "substitutions": [
        {
          "value": 170.0,
          "unit": "kPa",
          "symbol": "p_corner_pp"
        },
        {
          "value": 170.0,
          "unit": "kPa",
          "symbol": "p_corner_pm"
        },
        {
          "value": 170.0,
          "unit": "kPa",
          "symbol": "p_corner_mp"
        },
        {
          "value": 170.0,
          "unit": "kPa",
          "symbol": "p_corner_mm"
        }
      ],
      "result": {
        "value": 170.0,
        "unit": "kPa"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08."
      }
    },
    {
      "step_id": "edge_limit_multiplier",
      "expression": "edge_limit_multiplier",
      "substitutions": [],
      "result": {
        "value": 1.2,
        "unit": "1"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.26",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "table"
    },
    {
      "step_id": "edge_limit",
      "expression": "p_{edge,lim}=\\lambda_e R",
      "substitutions": [
        {
          "value": 1.2,
          "unit": "1",
          "symbol": "edge_limit_multiplier"
        },
        {
          "value": 152.02,
          "unit": "kPa",
          "symbol": "R"
        }
      ],
      "result": {
        "value": 182.424,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.26",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "step_id": "corner_limit_multiplier",
      "expression": "corner_limit_multiplier",
      "substitutions": [],
      "result": {
        "value": 1.5,
        "unit": "1"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.26",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "table"
    },
    {
      "step_id": "corner_limit",
      "expression": "p_{corner,lim}=\\lambda_c R",
      "substitutions": [
        {
          "value": 1.5,
          "unit": "1",
          "symbol": "corner_limit_multiplier"
        },
        {
          "value": 152.02,
          "unit": "kPa",
          "symbol": "R"
        }
      ],
      "result": {
        "value": 228.03000000000003,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.26",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "step_id": "p_le_R",
      "expression": "p \\le R",
      "substitutions": [
        {
          "value": 170.0,
          "unit": "kPa",
          "symbol": "p"
        },
        {
          "value": 152.02,
          "unit": "kPa",
          "symbol": "R"
        }
      ],
      "result": {
        "value": 170.0,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.7",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "check",
      "operator": "le",
      "right": {
        "value": 152.02,
        "unit": "kPa"
      },
      "passed": false
    },
    {
      "step_id": "p_x_max_le_limit",
      "expression": "p_x_max \\le edge_limit",
      "substitutions": [
        {
          "value": 170.0,
          "unit": "kPa",
          "symbol": "p_x_max"
        },
        {
          "value": 182.424,
          "unit": "kPa",
          "symbol": "edge_limit"
        }
      ],
      "result": {
        "value": 170.0,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.26",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "check",
      "operator": "le",
      "right": {
        "value": 182.424,
        "unit": "kPa"
      },
      "passed": true
    },
    {
      "step_id": "p_y_max_le_limit",
      "expression": "p_y_max \\le edge_limit",
      "substitutions": [
        {
          "value": 170.0,
          "unit": "kPa",
          "symbol": "p_y_max"
        },
        {
          "value": 182.424,
          "unit": "kPa",
          "symbol": "edge_limit"
        }
      ],
      "result": {
        "value": 170.0,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.26",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "check",
      "operator": "le",
      "right": {
        "value": 182.424,
        "unit": "kPa"
      },
      "passed": true
    },
    {
      "step_id": "p_corner_max_le_limit",
      "expression": "p_corner_max \\le corner_limit",
      "substitutions": [
        {
          "value": 170.0,
          "unit": "kPa",
          "symbol": "p_corner_max"
        },
        {
          "value": 228.03000000000003,
          "unit": "kPa",
          "symbol": "corner_limit"
        }
      ],
      "result": {
        "value": 170.0,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.26",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "check",
      "operator": "le",
      "right": {
        "value": 228.03000000000003,
        "unit": "kPa"
      },
      "passed": true
    }
  ],
  "unverified_step_count": 30,
  "result_id": "88888888-8888-4888-8888-888888888888",
  "parameter_source": {
    "kind": "interim",
    "data_sha256": "faaa0724af57ca6c8066f558c4e75c2785d099b34cbfb07c4a85892fdc3b68fe", // pragma: allowlist secret
    "profile": "strict"
  }
} satisfies ResultEnvelope

export const loadsFailJson = "{\"engine_version\":\"0.1.0\",\"input_hash\":\"14af66e093c1ab9096f1ef6952391443716d0c3ec9b2774dcce1b917d9379396\",\"outputs\":[{\"value\":152.02,\"unit\":\"kPa\",\"quantity\":\"R\",\"rounding_rule\":{\"decimals\":2,\"mode\":\"half_up\"},\"rounding_source\":{\"engineer\":\"Аким\",\"rationale\":\"Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются.\"}},{\"value\":170.0,\"unit\":\"kPa\",\"quantity\":\"p\",\"rounding_rule\":{\"decimals\":2,\"mode\":\"half_up\"},\"rounding_source\":{\"engineer\":\"Аким\",\"rationale\":\"Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются.\"}},{\"value\":170.0,\"unit\":\"kPa\",\"quantity\":\"p_x_min\",\"rounding_rule\":{\"decimals\":2,\"mode\":\"half_up\"},\"rounding_source\":{\"engineer\":\"Аким\",\"rationale\":\"Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются.\"}},{\"value\":170.0,\"unit\":\"kPa\",\"quantity\":\"p_x_max\",\"rounding_rule\":{\"decimals\":2,\"mode\":\"half_up\"},\"rounding_source\":{\"engineer\":\"Аким\",\"rationale\":\"Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются.\"}},{\"value\":170.0,\"unit\":\"kPa\",\"quantity\":\"p_y_min\",\"rounding_rule\":{\"decimals\":2,\"mode\":\"half_up\"},\"rounding_source\":{\"engineer\":\"Аким\",\"rationale\":\"Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются.\"}},{\"value\":170.0,\"unit\":\"kPa\",\"quantity\":\"p_y_max\",\"rounding_rule\":{\"decimals\":2,\"mode\":\"half_up\"},\"rounding_source\":{\"engineer\":\"Аким\",\"rationale\":\"Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются.\"}},{\"value\":170.0,\"unit\":\"kPa\",\"quantity\":\"p_corner_pp\",\"rounding_rule\":{\"decimals\":2,\"mode\":\"half_up\"},\"rounding_source\":{\"engineer\":\"Аким\",\"rationale\":\"Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются.\"}},{\"value\":170.0,\"unit\":\"kPa\",\"quantity\":\"p_corner_pm\",\"rounding_rule\":{\"decimals\":2,\"mode\":\"half_up\"},\"rounding_source\":{\"engineer\":\"Аким\",\"rationale\":\"Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются.\"}},{\"value\":170.0,\"unit\":\"kPa\",\"quantity\":\"p_corner_mp\",\"rounding_rule\":{\"decimals\":2,\"mode\":\"half_up\"},\"rounding_source\":{\"engineer\":\"Аким\",\"rationale\":\"Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются.\"}},{\"value\":170.0,\"unit\":\"kPa\",\"quantity\":\"p_corner_mm\",\"rounding_rule\":{\"decimals\":2,\"mode\":\"half_up\"},\"rounding_source\":{\"engineer\":\"Аким\",\"rationale\":\"Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются.\"}}],\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7, таблица 5.4\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"},{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7, экспликация k\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"},{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7, таблица 5.5\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"},{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7, экспликация k_z\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"},{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7, формула (5.7)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"},{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.28, explanation of formula (5.11)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"},{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.28, formula (5.11)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"},{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.28, applicability of formula (5.11)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"},{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.27, figure 5.1\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"},{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.29, formula (5.15)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"},{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.26\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"},{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"engineer_rules\":[{\"engineer\":\"Аким\",\"rationale\":\"Геометрия прямоугольной подошвы: A=b*l, Wx=l*b²/6, Wy=b*l²/6; инженерный контракт 2026-11-08.\"},{\"engineer\":\"Аким\",\"rationale\":\"Подписанный перенос нагрузок к подошве M_base=M+Q*h; оси x=b и y=l; инженерный контракт 2026-11-08.\"},{\"engineer\":\"Аким\",\"rationale\":\"Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08.\"},{\"engineer\":\"Аким\",\"rationale\":\"Полный контакт прямоугольной подошвы: минимум четырёх подписанных угловых давлений неотрицателен; решение инженера 2026-11-08.\"},{\"engineer\":\"Аким\",\"rationale\":\"Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются.\"}],\"verdict\":\"fail\",\"verdict_reason\":{\"kind\":\"check\",\"step_id\":\"p_le_R\"},\"warnings\":[],\"trace\":[{\"step_id\":\"gamma_c1\",\"expression\":\"\\\\gamma_{c1}\",\"substitutions\":[],\"result\":{\"value\":1.1,\"unit\":\"1\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7, таблица 5.4\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"table\"},{\"step_id\":\"gamma_c2\",\"expression\":\"\\\\gamma_{c2}\",\"substitutions\":[],\"result\":{\"value\":1.0,\"unit\":\"1\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7, таблица 5.4\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"table\"},{\"step_id\":\"k\",\"expression\":\"k\",\"substitutions\":[],\"result\":{\"value\":1.0,\"unit\":\"1\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7, экспликация k\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"table\"},{\"step_id\":\"M_gamma\",\"expression\":\"M_{\\\\gamma} = M_{\\\\gamma}\\\\left(\\\\varphi_{II}\\\\right)\",\"substitutions\":[{\"value\":20.0,\"unit\":\"deg\",\"symbol\":\"phi_II\"}],\"result\":{\"value\":0.51,\"unit\":\"1\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7, таблица 5.5\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"table\"},{\"step_id\":\"M_q\",\"expression\":\"M_{q} = M_{q}\\\\left(\\\\varphi_{II}\\\\right)\",\"substitutions\":[{\"value\":20.0,\"unit\":\"deg\",\"symbol\":\"phi_II\"}],\"result\":{\"value\":3.06,\"unit\":\"1\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7, таблица 5.5\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"table\"},{\"step_id\":\"M_c\",\"expression\":\"M_{c} = M_{c}\\\\left(\\\\varphi_{II}\\\\right)\",\"substitutions\":[{\"value\":20.0,\"unit\":\"deg\",\"symbol\":\"phi_II\"}],\"result\":{\"value\":5.66,\"unit\":\"1\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7, таблица 5.5\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"table\"},{\"step_id\":\"k_z\",\"expression\":\"k_{z}=1\",\"substitutions\":[],\"result\":{\"value\":1.0,\"unit\":\"1\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7, экспликация k_z\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"step_id\":\"R\",\"expression\":\"R=\\\\frac{\\\\gamma_{c1}\\\\gamma_{c2}}{k}\\\\left[M_{\\\\gamma}k_{z}b\\\\gamma_{II}+M_{q}d_{1}\\\\gamma'_{II}+(M_{q}-1)d_{b}\\\\gamma'_{II}+M_{c}c_{II}\\\\right]\",\"substitutions\":[{\"value\":1.1,\"unit\":\"1\",\"symbol\":\"gamma_c1\"},{\"value\":1.0,\"unit\":\"1\",\"symbol\":\"gamma_c2\"},{\"value\":1.0,\"unit\":\"1\",\"symbol\":\"k\"},{\"value\":0.51,\"unit\":\"1\",\"symbol\":\"M_gamma\"},{\"value\":1.0,\"unit\":\"1\",\"symbol\":\"k_z\"},{\"value\":2.0,\"unit\":\"m\",\"symbol\":\"b\"},{\"value\":20.0,\"unit\":\"kN/m3\",\"symbol\":\"gamma_II\"},{\"value\":3.06,\"unit\":\"1\",\"symbol\":\"M_q\"},{\"value\":1.0,\"unit\":\"m\",\"symbol\":\"d_1\"},{\"value\":20.0,\"unit\":\"kN/m3\",\"symbol\":\"gamma_II_prime\"},{\"value\":0.0,\"unit\":\"m\",\"symbol\":\"d_b\"},{\"value\":5.66,\"unit\":\"1\",\"symbol\":\"M_c\"},{\"value\":10.0,\"unit\":\"kPa\",\"symbol\":\"c_II\"}],\"result\":{\"value\":152.02,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7, формула (5.7)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"kind\":\"engineer_formula\",\"step_id\":\"A\",\"expression\":\"A=b l\",\"substitutions\":[{\"value\":2.0,\"unit\":\"m\",\"symbol\":\"b\"},{\"value\":3.0,\"unit\":\"m\",\"symbol\":\"l\"}],\"result\":{\"value\":6.0,\"unit\":\"m2\"},\"source\":{\"engineer\":\"Аким\",\"rationale\":\"Геометрия прямоугольной подошвы: A=b*l, Wx=l*b²/6, Wy=b*l²/6; инженерный контракт 2026-11-08.\"}},{\"kind\":\"engineer_formula\",\"step_id\":\"Wx\",\"expression\":\"W_x=l b^2/6\",\"substitutions\":[{\"value\":2.0,\"unit\":\"m\",\"symbol\":\"b\"},{\"value\":3.0,\"unit\":\"m\",\"symbol\":\"l\"}],\"result\":{\"value\":2.0,\"unit\":\"m3\"},\"source\":{\"engineer\":\"Аким\",\"rationale\":\"Геометрия прямоугольной подошвы: A=b*l, Wx=l*b²/6, Wy=b*l²/6; инженерный контракт 2026-11-08.\"}},{\"kind\":\"engineer_formula\",\"step_id\":\"Wy\",\"expression\":\"W_y=b l^2/6\",\"substitutions\":[{\"value\":2.0,\"unit\":\"m\",\"symbol\":\"b\"},{\"value\":3.0,\"unit\":\"m\",\"symbol\":\"l\"}],\"result\":{\"value\":3.0,\"unit\":\"m3\"},\"source\":{\"engineer\":\"Аким\",\"rationale\":\"Геометрия прямоугольной подошвы: A=b*l, Wx=l*b²/6, Wy=b*l²/6; инженерный контракт 2026-11-08.\"}},{\"kind\":\"engineer_formula\",\"step_id\":\"Mx_base\",\"expression\":\"M_{x,base}=M_x+Q_x h\",\"substitutions\":[{\"value\":0.0,\"unit\":\"kN*m\",\"symbol\":\"Mx\"},{\"value\":0.0,\"unit\":\"kN\",\"symbol\":\"Qx\"},{\"value\":1.0,\"unit\":\"m\",\"symbol\":\"h\"}],\"result\":{\"value\":0.0,\"unit\":\"kN*m\"},\"source\":{\"engineer\":\"Аким\",\"rationale\":\"Подписанный перенос нагрузок к подошве M_base=M+Q*h; оси x=b и y=l; инженерный контракт 2026-11-08.\"}},{\"kind\":\"engineer_formula\",\"step_id\":\"My_base\",\"expression\":\"M_{y,base}=M_y+Q_y h\",\"substitutions\":[{\"value\":0.0,\"unit\":\"kN*m\",\"symbol\":\"My\"},{\"value\":0.0,\"unit\":\"kN\",\"symbol\":\"Qy\"},{\"value\":1.0,\"unit\":\"m\",\"symbol\":\"h\"}],\"result\":{\"value\":0.0,\"unit\":\"kN*m\"},\"source\":{\"engineer\":\"Аким\",\"rationale\":\"Подписанный перенос нагрузок к подошве M_base=M+Q*h; оси x=b и y=l; инженерный контракт 2026-11-08.\"}},{\"step_id\":\"gamma_mt\",\"expression\":\"\\\\gamma_{mt}\",\"substitutions\":[],\"result\":{\"value\":20.0,\"unit\":\"kN/m3\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.28, explanation of formula (5.11)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"table\"},{\"step_id\":\"p\",\"expression\":\"p_{+}=\\\\frac{N}{A}+\\\\gamma_{mt}d+\\\\frac{M}{W}\",\"substitutions\":[{\"value\":900.0,\"unit\":\"kN\",\"symbol\":\"N\"},{\"value\":6.0,\"unit\":\"m2\",\"symbol\":\"A\"},{\"value\":20.0,\"unit\":\"kN/m3\",\"symbol\":\"gamma_mt\"},{\"value\":1.0,\"unit\":\"m\",\"symbol\":\"d\"},{\"value\":0.0,\"unit\":\"kN*m\",\"symbol\":\"M\"},{\"value\":2.0,\"unit\":\"m3\",\"symbol\":\"W\"}],\"result\":{\"value\":170.0,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.28, formula (5.11)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"kind\":\"engineer_formula\",\"step_id\":\"V\",\"expression\":\"V=N+\\\\gamma_{mt} d A\",\"substitutions\":[{\"value\":900.0,\"unit\":\"kN\",\"symbol\":\"N\"},{\"value\":20.0,\"unit\":\"kN/m3\",\"symbol\":\"gamma_mt\"},{\"value\":1.0,\"unit\":\"m\",\"symbol\":\"d\"},{\"value\":6.0,\"unit\":\"m2\",\"symbol\":\"A\"}],\"result\":{\"value\":1020.0,\"unit\":\"kN\"},\"source\":{\"engineer\":\"Аким\",\"rationale\":\"Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08.\"}},{\"step_id\":\"p_x_min\",\"expression\":\"p_{-}=\\\\frac{N}{A}+\\\\gamma_{mt}d-\\\\frac{M}{W}\",\"substitutions\":[{\"value\":900.0,\"unit\":\"kN\",\"symbol\":\"N\"},{\"value\":6.0,\"unit\":\"m2\",\"symbol\":\"A\"},{\"value\":20.0,\"unit\":\"kN/m3\",\"symbol\":\"gamma_mt\"},{\"value\":1.0,\"unit\":\"m\",\"symbol\":\"d\"},{\"value\":0.0,\"unit\":\"kN*m\",\"symbol\":\"M\"},{\"value\":2.0,\"unit\":\"m3\",\"symbol\":\"W\"}],\"result\":{\"value\":170.0,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.28, formula (5.11)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"step_id\":\"p_x_max\",\"expression\":\"p_{+}=\\\\frac{N}{A}+\\\\gamma_{mt}d+\\\\frac{M}{W}\",\"substitutions\":[{\"value\":900.0,\"unit\":\"kN\",\"symbol\":\"N\"},{\"value\":6.0,\"unit\":\"m2\",\"symbol\":\"A\"},{\"value\":20.0,\"unit\":\"kN/m3\",\"symbol\":\"gamma_mt\"},{\"value\":1.0,\"unit\":\"m\",\"symbol\":\"d\"},{\"value\":0.0,\"unit\":\"kN*m\",\"symbol\":\"M\"},{\"value\":2.0,\"unit\":\"m3\",\"symbol\":\"W\"}],\"result\":{\"value\":170.0,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.28, formula (5.11)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"kind\":\"engineer_formula\",\"step_id\":\"e_x\",\"expression\":\"e_x=|M_{x,base}|/V\",\"substitutions\":[{\"value\":0.0,\"unit\":\"kN*m\",\"symbol\":\"Mx_base\"},{\"value\":1020.0,\"unit\":\"kN\",\"symbol\":\"V\"}],\"result\":{\"value\":0.0,\"unit\":\"m\"},\"source\":{\"engineer\":\"Аким\",\"rationale\":\"Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08.\"}},{\"step_id\":\"relative_eccentricity_x\",\"expression\":\"e/l\\\\leq1/6\",\"substitutions\":[{\"value\":0.0,\"unit\":\"1\",\"symbol\":\"e/L\"},{\"value\":1.0,\"unit\":\"1\",\"symbol\":\"numerator\"},{\"value\":6.0,\"unit\":\"1\",\"symbol\":\"denominator\"}],\"result\":{\"value\":1.0,\"unit\":\"1\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.28, applicability of formula (5.11)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"step_id\":\"pressure_diagram_x\",\"expression\":\"e<l/6\",\"substitutions\":[{\"value\":0.0,\"unit\":\"m\",\"symbol\":\"e\"},{\"value\":2.0,\"unit\":\"m\",\"symbol\":\"l\"}],\"result\":{\"value\":0.0,\"unit\":\"m\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.27, figure 5.1\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"step_id\":\"p_y_min\",\"expression\":\"p_{-}=\\\\frac{N}{A}+\\\\gamma_{mt}d-\\\\frac{M}{W}\",\"substitutions\":[{\"value\":900.0,\"unit\":\"kN\",\"symbol\":\"N\"},{\"value\":6.0,\"unit\":\"m2\",\"symbol\":\"A\"},{\"value\":20.0,\"unit\":\"kN/m3\",\"symbol\":\"gamma_mt\"},{\"value\":1.0,\"unit\":\"m\",\"symbol\":\"d\"},{\"value\":0.0,\"unit\":\"kN*m\",\"symbol\":\"M\"},{\"value\":3.0,\"unit\":\"m3\",\"symbol\":\"W\"}],\"result\":{\"value\":170.0,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.28, formula (5.11)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"step_id\":\"p_y_max\",\"expression\":\"p_{+}=\\\\frac{N}{A}+\\\\gamma_{mt}d+\\\\frac{M}{W}\",\"substitutions\":[{\"value\":900.0,\"unit\":\"kN\",\"symbol\":\"N\"},{\"value\":6.0,\"unit\":\"m2\",\"symbol\":\"A\"},{\"value\":20.0,\"unit\":\"kN/m3\",\"symbol\":\"gamma_mt\"},{\"value\":1.0,\"unit\":\"m\",\"symbol\":\"d\"},{\"value\":0.0,\"unit\":\"kN*m\",\"symbol\":\"M\"},{\"value\":3.0,\"unit\":\"m3\",\"symbol\":\"W\"}],\"result\":{\"value\":170.0,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.28, formula (5.11)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"kind\":\"engineer_formula\",\"step_id\":\"e_y\",\"expression\":\"e_y=|M_{y,base}|/V\",\"substitutions\":[{\"value\":0.0,\"unit\":\"kN*m\",\"symbol\":\"My_base\"},{\"value\":1020.0,\"unit\":\"kN\",\"symbol\":\"V\"}],\"result\":{\"value\":0.0,\"unit\":\"m\"},\"source\":{\"engineer\":\"Аким\",\"rationale\":\"Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08.\"}},{\"step_id\":\"relative_eccentricity_y\",\"expression\":\"e/l\\\\leq1/6\",\"substitutions\":[{\"value\":0.0,\"unit\":\"1\",\"symbol\":\"e/L\"},{\"value\":1.0,\"unit\":\"1\",\"symbol\":\"numerator\"},{\"value\":6.0,\"unit\":\"1\",\"symbol\":\"denominator\"}],\"result\":{\"value\":1.0,\"unit\":\"1\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.28, applicability of formula (5.11)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"step_id\":\"pressure_diagram_y\",\"expression\":\"e<l/6\",\"substitutions\":[{\"value\":0.0,\"unit\":\"m\",\"symbol\":\"e\"},{\"value\":3.0,\"unit\":\"m\",\"symbol\":\"l\"}],\"result\":{\"value\":0.0,\"unit\":\"m\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.27, figure 5.1\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"step_id\":\"corner_component_pp\",\"expression\":\"P_{\\\\max}=\\\\frac{N}{A}+\\\\gamma_{mt}d+\\\\frac{M_x}{W_x}+\\\\frac{M_y}{W_y}\",\"substitutions\":[{\"value\":900.0,\"unit\":\"kN\",\"symbol\":\"N\"},{\"value\":6.0,\"unit\":\"m2\",\"symbol\":\"A\"},{\"value\":20.0,\"unit\":\"kN/m3\",\"symbol\":\"gamma_mt\"},{\"value\":1.0,\"unit\":\"m\",\"symbol\":\"d\"},{\"value\":0.0,\"unit\":\"kN*m\",\"symbol\":\"M_x\"},{\"value\":2.0,\"unit\":\"m3\",\"symbol\":\"W_x\"},{\"value\":0.0,\"unit\":\"kN*m\",\"symbol\":\"M_y\"},{\"value\":3.0,\"unit\":\"m3\",\"symbol\":\"W_y\"}],\"result\":{\"value\":170.0,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.29, formula (5.15)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"kind\":\"engineer_formula\",\"step_id\":\"p_corner_pp\",\"expression\":\"p_{pp}=p+s_x M_{x,base}/W_x+s_y M_{y,base}/W_y\",\"substitutions\":[{\"value\":170.0,\"unit\":\"kPa\",\"symbol\":\"p\"},{\"value\":0.0,\"unit\":\"kN*m\",\"symbol\":\"Mx_base\"},{\"value\":2.0,\"unit\":\"m3\",\"symbol\":\"Wx\"},{\"value\":0.0,\"unit\":\"kN*m\",\"symbol\":\"My_base\"},{\"value\":3.0,\"unit\":\"m3\",\"symbol\":\"Wy\"},{\"value\":1.0,\"unit\":\"1\",\"symbol\":\"sign_x_pp\"},{\"value\":1.0,\"unit\":\"1\",\"symbol\":\"sign_y_pp\"},{\"value\":170.0,\"unit\":\"kPa\",\"symbol\":\"corner_component_pp\"}],\"result\":{\"value\":170.0,\"unit\":\"kPa\"},\"source\":{\"engineer\":\"Аким\",\"rationale\":\"Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08.\"}},{\"step_id\":\"corner_component_pm\",\"expression\":\"P_{\\\\max}=\\\\frac{N}{A}+\\\\gamma_{mt}d+\\\\frac{M_x}{W_x}+\\\\frac{M_y}{W_y}\",\"substitutions\":[{\"value\":900.0,\"unit\":\"kN\",\"symbol\":\"N\"},{\"value\":6.0,\"unit\":\"m2\",\"symbol\":\"A\"},{\"value\":20.0,\"unit\":\"kN/m3\",\"symbol\":\"gamma_mt\"},{\"value\":1.0,\"unit\":\"m\",\"symbol\":\"d\"},{\"value\":0.0,\"unit\":\"kN*m\",\"symbol\":\"M_x\"},{\"value\":2.0,\"unit\":\"m3\",\"symbol\":\"W_x\"},{\"value\":-0.0,\"unit\":\"kN*m\",\"symbol\":\"M_y\"},{\"value\":3.0,\"unit\":\"m3\",\"symbol\":\"W_y\"}],\"result\":{\"value\":170.0,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.29, formula (5.15)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"kind\":\"engineer_formula\",\"step_id\":\"p_corner_pm\",\"expression\":\"p_{pm}=p+s_x M_{x,base}/W_x+s_y M_{y,base}/W_y\",\"substitutions\":[{\"value\":170.0,\"unit\":\"kPa\",\"symbol\":\"p\"},{\"value\":0.0,\"unit\":\"kN*m\",\"symbol\":\"Mx_base\"},{\"value\":2.0,\"unit\":\"m3\",\"symbol\":\"Wx\"},{\"value\":0.0,\"unit\":\"kN*m\",\"symbol\":\"My_base\"},{\"value\":3.0,\"unit\":\"m3\",\"symbol\":\"Wy\"},{\"value\":1.0,\"unit\":\"1\",\"symbol\":\"sign_x_pm\"},{\"value\":-1.0,\"unit\":\"1\",\"symbol\":\"sign_y_pm\"},{\"value\":170.0,\"unit\":\"kPa\",\"symbol\":\"corner_component_pm\"}],\"result\":{\"value\":170.0,\"unit\":\"kPa\"},\"source\":{\"engineer\":\"Аким\",\"rationale\":\"Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08.\"}},{\"step_id\":\"corner_component_mp\",\"expression\":\"P_{\\\\max}=\\\\frac{N}{A}+\\\\gamma_{mt}d+\\\\frac{M_x}{W_x}+\\\\frac{M_y}{W_y}\",\"substitutions\":[{\"value\":900.0,\"unit\":\"kN\",\"symbol\":\"N\"},{\"value\":6.0,\"unit\":\"m2\",\"symbol\":\"A\"},{\"value\":20.0,\"unit\":\"kN/m3\",\"symbol\":\"gamma_mt\"},{\"value\":1.0,\"unit\":\"m\",\"symbol\":\"d\"},{\"value\":-0.0,\"unit\":\"kN*m\",\"symbol\":\"M_x\"},{\"value\":2.0,\"unit\":\"m3\",\"symbol\":\"W_x\"},{\"value\":0.0,\"unit\":\"kN*m\",\"symbol\":\"M_y\"},{\"value\":3.0,\"unit\":\"m3\",\"symbol\":\"W_y\"}],\"result\":{\"value\":170.0,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.29, formula (5.15)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"kind\":\"engineer_formula\",\"step_id\":\"p_corner_mp\",\"expression\":\"p_{mp}=p+s_x M_{x,base}/W_x+s_y M_{y,base}/W_y\",\"substitutions\":[{\"value\":170.0,\"unit\":\"kPa\",\"symbol\":\"p\"},{\"value\":0.0,\"unit\":\"kN*m\",\"symbol\":\"Mx_base\"},{\"value\":2.0,\"unit\":\"m3\",\"symbol\":\"Wx\"},{\"value\":0.0,\"unit\":\"kN*m\",\"symbol\":\"My_base\"},{\"value\":3.0,\"unit\":\"m3\",\"symbol\":\"Wy\"},{\"value\":-1.0,\"unit\":\"1\",\"symbol\":\"sign_x_mp\"},{\"value\":1.0,\"unit\":\"1\",\"symbol\":\"sign_y_mp\"},{\"value\":170.0,\"unit\":\"kPa\",\"symbol\":\"corner_component_mp\"}],\"result\":{\"value\":170.0,\"unit\":\"kPa\"},\"source\":{\"engineer\":\"Аким\",\"rationale\":\"Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08.\"}},{\"step_id\":\"corner_component_mm\",\"expression\":\"P_{\\\\max}=\\\\frac{N}{A}+\\\\gamma_{mt}d+\\\\frac{M_x}{W_x}+\\\\frac{M_y}{W_y}\",\"substitutions\":[{\"value\":900.0,\"unit\":\"kN\",\"symbol\":\"N\"},{\"value\":6.0,\"unit\":\"m2\",\"symbol\":\"A\"},{\"value\":20.0,\"unit\":\"kN/m3\",\"symbol\":\"gamma_mt\"},{\"value\":1.0,\"unit\":\"m\",\"symbol\":\"d\"},{\"value\":-0.0,\"unit\":\"kN*m\",\"symbol\":\"M_x\"},{\"value\":2.0,\"unit\":\"m3\",\"symbol\":\"W_x\"},{\"value\":-0.0,\"unit\":\"kN*m\",\"symbol\":\"M_y\"},{\"value\":3.0,\"unit\":\"m3\",\"symbol\":\"W_y\"}],\"result\":{\"value\":170.0,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.29, formula (5.15)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"kind\":\"engineer_formula\",\"step_id\":\"p_corner_mm\",\"expression\":\"p_{mm}=p+s_x M_{x,base}/W_x+s_y M_{y,base}/W_y\",\"substitutions\":[{\"value\":170.0,\"unit\":\"kPa\",\"symbol\":\"p\"},{\"value\":0.0,\"unit\":\"kN*m\",\"symbol\":\"Mx_base\"},{\"value\":2.0,\"unit\":\"m3\",\"symbol\":\"Wx\"},{\"value\":0.0,\"unit\":\"kN*m\",\"symbol\":\"My_base\"},{\"value\":3.0,\"unit\":\"m3\",\"symbol\":\"Wy\"},{\"value\":-1.0,\"unit\":\"1\",\"symbol\":\"sign_x_mm\"},{\"value\":-1.0,\"unit\":\"1\",\"symbol\":\"sign_y_mm\"},{\"value\":170.0,\"unit\":\"kPa\",\"symbol\":\"corner_component_mm\"}],\"result\":{\"value\":170.0,\"unit\":\"kPa\"},\"source\":{\"engineer\":\"Аким\",\"rationale\":\"Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08.\"}},{\"kind\":\"engineer_formula\",\"step_id\":\"p_corner_min\",\"expression\":\"p_{corner,min}=\\\\min(p_{++},p_{+-},p_{-+},p_{--})\",\"substitutions\":[{\"value\":170.0,\"unit\":\"kPa\",\"symbol\":\"p_corner_pp\"},{\"value\":170.0,\"unit\":\"kPa\",\"symbol\":\"p_corner_pm\"},{\"value\":170.0,\"unit\":\"kPa\",\"symbol\":\"p_corner_mp\"},{\"value\":170.0,\"unit\":\"kPa\",\"symbol\":\"p_corner_mm\"}],\"result\":{\"value\":170.0,\"unit\":\"kPa\"},\"source\":{\"engineer\":\"Аким\",\"rationale\":\"Полный контакт прямоугольной подошвы: минимум четырёх подписанных угловых давлений неотрицателен; решение инженера 2026-11-08.\"}},{\"kind\":\"engineer_formula\",\"step_id\":\"p_corner_max\",\"expression\":\"p_{corner,max}=\\\\max(p_{++},p_{+-},p_{-+},p_{--})\",\"substitutions\":[{\"value\":170.0,\"unit\":\"kPa\",\"symbol\":\"p_corner_pp\"},{\"value\":170.0,\"unit\":\"kPa\",\"symbol\":\"p_corner_pm\"},{\"value\":170.0,\"unit\":\"kPa\",\"symbol\":\"p_corner_mp\"},{\"value\":170.0,\"unit\":\"kPa\",\"symbol\":\"p_corner_mm\"}],\"result\":{\"value\":170.0,\"unit\":\"kPa\"},\"source\":{\"engineer\":\"Аким\",\"rationale\":\"Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08.\"}},{\"step_id\":\"edge_limit_multiplier\",\"expression\":\"edge_limit_multiplier\",\"substitutions\":[],\"result\":{\"value\":1.2,\"unit\":\"1\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.26\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"table\"},{\"step_id\":\"edge_limit\",\"expression\":\"p_{edge,lim}=\\\\lambda_e R\",\"substitutions\":[{\"value\":1.2,\"unit\":\"1\",\"symbol\":\"edge_limit_multiplier\"},{\"value\":152.02,\"unit\":\"kPa\",\"symbol\":\"R\"}],\"result\":{\"value\":182.424,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.26\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"step_id\":\"corner_limit_multiplier\",\"expression\":\"corner_limit_multiplier\",\"substitutions\":[],\"result\":{\"value\":1.5,\"unit\":\"1\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.26\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"table\"},{\"step_id\":\"corner_limit\",\"expression\":\"p_{corner,lim}=\\\\lambda_c R\",\"substitutions\":[{\"value\":1.5,\"unit\":\"1\",\"symbol\":\"corner_limit_multiplier\"},{\"value\":152.02,\"unit\":\"kPa\",\"symbol\":\"R\"}],\"result\":{\"value\":228.03000000000003,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.26\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"step_id\":\"p_le_R\",\"expression\":\"p \\\\le R\",\"substitutions\":[{\"value\":170.0,\"unit\":\"kPa\",\"symbol\":\"p\"},{\"value\":152.02,\"unit\":\"kPa\",\"symbol\":\"R\"}],\"result\":{\"value\":170.0,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"check\",\"operator\":\"le\",\"right\":{\"value\":152.02,\"unit\":\"kPa\"},\"passed\":false},{\"step_id\":\"p_x_max_le_limit\",\"expression\":\"p_x_max \\\\le edge_limit\",\"substitutions\":[{\"value\":170.0,\"unit\":\"kPa\",\"symbol\":\"p_x_max\"},{\"value\":182.424,\"unit\":\"kPa\",\"symbol\":\"edge_limit\"}],\"result\":{\"value\":170.0,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.26\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"check\",\"operator\":\"le\",\"right\":{\"value\":182.424,\"unit\":\"kPa\"},\"passed\":true},{\"step_id\":\"p_y_max_le_limit\",\"expression\":\"p_y_max \\\\le edge_limit\",\"substitutions\":[{\"value\":170.0,\"unit\":\"kPa\",\"symbol\":\"p_y_max\"},{\"value\":182.424,\"unit\":\"kPa\",\"symbol\":\"edge_limit\"}],\"result\":{\"value\":170.0,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.26\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"check\",\"operator\":\"le\",\"right\":{\"value\":182.424,\"unit\":\"kPa\"},\"passed\":true},{\"step_id\":\"p_corner_max_le_limit\",\"expression\":\"p_corner_max \\\\le corner_limit\",\"substitutions\":[{\"value\":170.0,\"unit\":\"kPa\",\"symbol\":\"p_corner_max\"},{\"value\":228.03000000000003,\"unit\":\"kPa\",\"symbol\":\"corner_limit\"}],\"result\":{\"value\":170.0,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.26\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"check\",\"operator\":\"le\",\"right\":{\"value\":228.03000000000003,\"unit\":\"kPa\"},\"passed\":true}],\"unverified_step_count\":30,\"result_id\":\"88888888-8888-4888-8888-888888888888\",\"parameter_source\":{\"kind\":\"interim\",\"data_sha256\":\"faaa0724af57ca6c8066f558c4e75c2785d099b34cbfb07c4a85892fdc3b68fe\",\"profile\":\"strict\"}}"

export const LOADS_BOUND_REFUSAL_ID = '99999999-9999-4999-8999-999999999999'

export const loadsBoundRefusalInputs = {
  "b": {
    "value": 2,
    "unit": "m"
  },
  "d_1": {
    "value": 1,
    "unit": "m"
  },
  "d_b": {
    "value": 3,
    "unit": "m"
  },
  "gamma_II": {
    "value": 20,
    "unit": "kN/m3"
  },
  "gamma_II_prime": {
    "value": 20,
    "unit": "kN/m3"
  },
  "c_II": {
    "value": 10,
    "unit": "kPa"
  },
  "phi_II": {
    "value": 20,
    "unit": "deg"
  },
  "l": {
    "value": 3,
    "unit": "m"
  },
  "h": {
    "value": 1,
    "unit": "m"
  },
  "d": {
    "value": 1,
    "unit": "m"
  },
  "N": {
    "value": 600,
    "unit": "kN"
  },
  "Mx": {
    "value": 0,
    "unit": "kN*m"
  },
  "My": {
    "value": 0,
    "unit": "kN*m"
  },
  "Qx": {
    "value": 0,
    "unit": "kN"
  },
  "Qy": {
    "value": 0,
    "unit": "kN"
  }
} satisfies CalculationRequest['inputs']

export const loadsBoundRefusalEnvelope = {
  "engine_version": "0.1.0",
  "input_hash": "9b2a99a09d56cd892ec63369f32eda19d55692f72c42acfcd7b59258aba8b41c", // pragma: allowlist secret
  "outputs": [],
  "norm_refs": [
    {
      "document": "СП 22.13330.2016",
      "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
      "clause": "5.6.7, экспликация d_b",
      "status": "unverified",
      "provenance": "machine-extracted"
    }
  ],
  "engineer_rules": [],
  "verdict": "refused",
  "verdict_reason": {
    "kind": "bound",
    "value": {
      "value": 3.0,
      "unit": "m"
    },
    "bound": {
      "quantity": "d_b",
      "kind": "max",
      "value": 2.0,
      "inclusive": true,
      "source": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.7, экспликация d_b",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ]
    }
  },
  "warnings": [],
  "trace": [],
  "unverified_step_count": 0,
  "result_id": "99999999-9999-4999-8999-999999999999",
  "parameter_source": {
    "kind": "interim",
    "data_sha256": "faaa0724af57ca6c8066f558c4e75c2785d099b34cbfb07c4a85892fdc3b68fe", // pragma: allowlist secret
    "profile": "strict"
  }
} satisfies ResultEnvelope

export const loadsBoundRefusalJson = "{\"engine_version\":\"0.1.0\",\"input_hash\":\"9b2a99a09d56cd892ec63369f32eda19d55692f72c42acfcd7b59258aba8b41c\",\"outputs\":[],\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7, экспликация d_b\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"engineer_rules\":[],\"verdict\":\"refused\",\"verdict_reason\":{\"kind\":\"bound\",\"value\":{\"value\":3.0,\"unit\":\"m\"},\"bound\":{\"quantity\":\"d_b\",\"kind\":\"max\",\"value\":2.0,\"inclusive\":true,\"source\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7, экспликация d_b\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}]}},\"warnings\":[],\"trace\":[],\"unverified_step_count\":0,\"result_id\":\"99999999-9999-4999-8999-999999999999\",\"parameter_source\":{\"kind\":\"interim\",\"data_sha256\":\"faaa0724af57ca6c8066f558c4e75c2785d099b34cbfb07c4a85892fdc3b68fe\",\"profile\":\"strict\"}}"

export const LOADS_CONTACT_REFUSAL_ID = 'aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa'

export const loadsContactRefusalInputs = {
  "b": {
    "value": 2,
    "unit": "m"
  },
  "d_1": {
    "value": 1,
    "unit": "m"
  },
  "d_b": {
    "value": 0,
    "unit": "m"
  },
  "gamma_II": {
    "value": 20,
    "unit": "kN/m3"
  },
  "gamma_II_prime": {
    "value": 20,
    "unit": "kN/m3"
  },
  "c_II": {
    "value": 10,
    "unit": "kPa"
  },
  "phi_II": {
    "value": 20,
    "unit": "deg"
  },
  "l": {
    "value": 3,
    "unit": "m"
  },
  "h": {
    "value": 1,
    "unit": "m"
  },
  "d": {
    "value": 1,
    "unit": "m"
  },
  "N": {
    "value": 600,
    "unit": "kN"
  },
  "Mx": {
    "value": 180,
    "unit": "kN*m"
  },
  "My": {
    "value": 180,
    "unit": "kN*m"
  },
  "Qx": {
    "value": 0,
    "unit": "kN"
  },
  "Qy": {
    "value": 0,
    "unit": "kN"
  }
} satisfies CalculationRequest['inputs']

export const loadsContactRefusalEnvelope = {
  "engine_version": "0.1.0",
  "input_hash": "f4b13a8543416777e9a56a89b3e498631219a7ef77ceff19a3a9b5da628076b5", // pragma: allowlist secret
  "outputs": [],
  "norm_refs": [
    {
      "document": "СП 22.13330.2016",
      "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
      "clause": "5.6.7, таблица 5.4",
      "status": "unverified",
      "provenance": "machine-extracted"
    },
    {
      "document": "СП 22.13330.2016",
      "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
      "clause": "5.6.7, экспликация k",
      "status": "unverified",
      "provenance": "machine-extracted"
    },
    {
      "document": "СП 22.13330.2016",
      "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
      "clause": "5.6.7, таблица 5.5",
      "status": "unverified",
      "provenance": "machine-extracted"
    },
    {
      "document": "СП 22.13330.2016",
      "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
      "clause": "5.6.7, экспликация k_z",
      "status": "unverified",
      "provenance": "machine-extracted"
    },
    {
      "document": "СП 22.13330.2016",
      "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
      "clause": "5.6.7, формула (5.7)",
      "status": "unverified",
      "provenance": "machine-extracted"
    },
    {
      "document": "СП 22.13330.2016",
      "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
      "clause": "5.6.28, explanation of formula (5.11)",
      "status": "unverified",
      "provenance": "machine-extracted"
    },
    {
      "document": "СП 22.13330.2016",
      "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
      "clause": "5.6.28, formula (5.11)",
      "status": "unverified",
      "provenance": "machine-extracted"
    },
    {
      "document": "СП 22.13330.2016",
      "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
      "clause": "5.6.28, applicability of formula (5.11)",
      "status": "unverified",
      "provenance": "machine-extracted"
    },
    {
      "document": "СП 22.13330.2016",
      "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
      "clause": "5.6.27, figure 5.1",
      "status": "unverified",
      "provenance": "machine-extracted"
    },
    {
      "document": "СП 22.13330.2016",
      "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
      "clause": "5.6.29, formula (5.15)",
      "status": "unverified",
      "provenance": "machine-extracted"
    }
  ],
  "engineer_rules": [
    {
      "engineer": "Аким",
      "rationale": "Геометрия прямоугольной подошвы: A=b*l, Wx=l*b²/6, Wy=b*l²/6; инженерный контракт 2026-11-08."
    },
    {
      "engineer": "Аким",
      "rationale": "Подписанный перенос нагрузок к подошве M_base=M+Q*h; оси x=b и y=l; инженерный контракт 2026-11-08."
    },
    {
      "engineer": "Аким",
      "rationale": "Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08."
    },
    {
      "engineer": "Аким",
      "rationale": "Полный контакт прямоугольной подошвы: минимум четырёх подписанных угловых давлений неотрицателен; решение инженера 2026-11-08."
    }
  ],
  "verdict": "refused",
  "verdict_reason": {
    "kind": "derived",
    "check_id": "full_contact",
    "step_id": "p_corner_min",
    "quantity": "p_corner_min",
    "value": {
      "value": -30.0,
      "unit": "kPa"
    },
    "operator": "ge",
    "limit": {
      "value": 0.0,
      "unit": "kPa"
    },
    "source": {
      "engineer": "Аким",
      "rationale": "Полный контакт прямоугольной подошвы: минимум четырёх подписанных угловых давлений неотрицателен; решение инженера 2026-11-08."
    },
    "related_inputs": [
      "N",
      "Mx",
      "My",
      "Qx",
      "Qy",
      "h",
      "b",
      "l",
      "d"
    ],
    "limiting_corner": "mm"
  },
  "warnings": [],
  "trace": [
    {
      "step_id": "gamma_c1",
      "expression": "\\gamma_{c1}",
      "substitutions": [],
      "result": {
        "value": 1.1,
        "unit": "1"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.7, таблица 5.4",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "table"
    },
    {
      "step_id": "gamma_c2",
      "expression": "\\gamma_{c2}",
      "substitutions": [],
      "result": {
        "value": 1.0,
        "unit": "1"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.7, таблица 5.4",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "table"
    },
    {
      "step_id": "k",
      "expression": "k",
      "substitutions": [],
      "result": {
        "value": 1.0,
        "unit": "1"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.7, экспликация k",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "table"
    },
    {
      "step_id": "M_gamma",
      "expression": "M_{\\gamma} = M_{\\gamma}\\left(\\varphi_{II}\\right)",
      "substitutions": [
        {
          "value": 20.0,
          "unit": "deg",
          "symbol": "phi_II"
        }
      ],
      "result": {
        "value": 0.51,
        "unit": "1"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.7, таблица 5.5",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "table"
    },
    {
      "step_id": "M_q",
      "expression": "M_{q} = M_{q}\\left(\\varphi_{II}\\right)",
      "substitutions": [
        {
          "value": 20.0,
          "unit": "deg",
          "symbol": "phi_II"
        }
      ],
      "result": {
        "value": 3.06,
        "unit": "1"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.7, таблица 5.5",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "table"
    },
    {
      "step_id": "M_c",
      "expression": "M_{c} = M_{c}\\left(\\varphi_{II}\\right)",
      "substitutions": [
        {
          "value": 20.0,
          "unit": "deg",
          "symbol": "phi_II"
        }
      ],
      "result": {
        "value": 5.66,
        "unit": "1"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.7, таблица 5.5",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "table"
    },
    {
      "step_id": "k_z",
      "expression": "k_{z}=1",
      "substitutions": [],
      "result": {
        "value": 1.0,
        "unit": "1"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.7, экспликация k_z",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "step_id": "R",
      "expression": "R=\\frac{\\gamma_{c1}\\gamma_{c2}}{k}\\left[M_{\\gamma}k_{z}b\\gamma_{II}+M_{q}d_{1}\\gamma'_{II}+(M_{q}-1)d_{b}\\gamma'_{II}+M_{c}c_{II}\\right]",
      "substitutions": [
        {
          "value": 1.1,
          "unit": "1",
          "symbol": "gamma_c1"
        },
        {
          "value": 1.0,
          "unit": "1",
          "symbol": "gamma_c2"
        },
        {
          "value": 1.0,
          "unit": "1",
          "symbol": "k"
        },
        {
          "value": 0.51,
          "unit": "1",
          "symbol": "M_gamma"
        },
        {
          "value": 1.0,
          "unit": "1",
          "symbol": "k_z"
        },
        {
          "value": 2.0,
          "unit": "m",
          "symbol": "b"
        },
        {
          "value": 20.0,
          "unit": "kN/m3",
          "symbol": "gamma_II"
        },
        {
          "value": 3.06,
          "unit": "1",
          "symbol": "M_q"
        },
        {
          "value": 1.0,
          "unit": "m",
          "symbol": "d_1"
        },
        {
          "value": 20.0,
          "unit": "kN/m3",
          "symbol": "gamma_II_prime"
        },
        {
          "value": 0.0,
          "unit": "m",
          "symbol": "d_b"
        },
        {
          "value": 5.66,
          "unit": "1",
          "symbol": "M_c"
        },
        {
          "value": 10.0,
          "unit": "kPa",
          "symbol": "c_II"
        }
      ],
      "result": {
        "value": 152.02,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.7, формула (5.7)",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "kind": "engineer_formula",
      "step_id": "A",
      "expression": "A=b l",
      "substitutions": [
        {
          "value": 2.0,
          "unit": "m",
          "symbol": "b"
        },
        {
          "value": 3.0,
          "unit": "m",
          "symbol": "l"
        }
      ],
      "result": {
        "value": 6.0,
        "unit": "m2"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Геометрия прямоугольной подошвы: A=b*l, Wx=l*b²/6, Wy=b*l²/6; инженерный контракт 2026-11-08."
      }
    },
    {
      "kind": "engineer_formula",
      "step_id": "Wx",
      "expression": "W_x=l b^2/6",
      "substitutions": [
        {
          "value": 2.0,
          "unit": "m",
          "symbol": "b"
        },
        {
          "value": 3.0,
          "unit": "m",
          "symbol": "l"
        }
      ],
      "result": {
        "value": 2.0,
        "unit": "m3"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Геометрия прямоугольной подошвы: A=b*l, Wx=l*b²/6, Wy=b*l²/6; инженерный контракт 2026-11-08."
      }
    },
    {
      "kind": "engineer_formula",
      "step_id": "Wy",
      "expression": "W_y=b l^2/6",
      "substitutions": [
        {
          "value": 2.0,
          "unit": "m",
          "symbol": "b"
        },
        {
          "value": 3.0,
          "unit": "m",
          "symbol": "l"
        }
      ],
      "result": {
        "value": 3.0,
        "unit": "m3"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Геометрия прямоугольной подошвы: A=b*l, Wx=l*b²/6, Wy=b*l²/6; инженерный контракт 2026-11-08."
      }
    },
    {
      "kind": "engineer_formula",
      "step_id": "Mx_base",
      "expression": "M_{x,base}=M_x+Q_x h",
      "substitutions": [
        {
          "value": 180.0,
          "unit": "kN*m",
          "symbol": "Mx"
        },
        {
          "value": 0.0,
          "unit": "kN",
          "symbol": "Qx"
        },
        {
          "value": 1.0,
          "unit": "m",
          "symbol": "h"
        }
      ],
      "result": {
        "value": 180.0,
        "unit": "kN*m"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Подписанный перенос нагрузок к подошве M_base=M+Q*h; оси x=b и y=l; инженерный контракт 2026-11-08."
      }
    },
    {
      "kind": "engineer_formula",
      "step_id": "My_base",
      "expression": "M_{y,base}=M_y+Q_y h",
      "substitutions": [
        {
          "value": 180.0,
          "unit": "kN*m",
          "symbol": "My"
        },
        {
          "value": 0.0,
          "unit": "kN",
          "symbol": "Qy"
        },
        {
          "value": 1.0,
          "unit": "m",
          "symbol": "h"
        }
      ],
      "result": {
        "value": 180.0,
        "unit": "kN*m"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Подписанный перенос нагрузок к подошве M_base=M+Q*h; оси x=b и y=l; инженерный контракт 2026-11-08."
      }
    },
    {
      "step_id": "gamma_mt",
      "expression": "\\gamma_{mt}",
      "substitutions": [],
      "result": {
        "value": 20.0,
        "unit": "kN/m3"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.28, explanation of formula (5.11)",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "table"
    },
    {
      "step_id": "p",
      "expression": "p_{+}=\\frac{N}{A}+\\gamma_{mt}d+\\frac{M}{W}",
      "substitutions": [
        {
          "value": 600.0,
          "unit": "kN",
          "symbol": "N"
        },
        {
          "value": 6.0,
          "unit": "m2",
          "symbol": "A"
        },
        {
          "value": 20.0,
          "unit": "kN/m3",
          "symbol": "gamma_mt"
        },
        {
          "value": 1.0,
          "unit": "m",
          "symbol": "d"
        },
        {
          "value": 0.0,
          "unit": "kN*m",
          "symbol": "M"
        },
        {
          "value": 2.0,
          "unit": "m3",
          "symbol": "W"
        }
      ],
      "result": {
        "value": 120.0,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.28, formula (5.11)",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "kind": "engineer_formula",
      "step_id": "V",
      "expression": "V=N+\\gamma_{mt} d A",
      "substitutions": [
        {
          "value": 600.0,
          "unit": "kN",
          "symbol": "N"
        },
        {
          "value": 20.0,
          "unit": "kN/m3",
          "symbol": "gamma_mt"
        },
        {
          "value": 1.0,
          "unit": "m",
          "symbol": "d"
        },
        {
          "value": 6.0,
          "unit": "m2",
          "symbol": "A"
        }
      ],
      "result": {
        "value": 720.0,
        "unit": "kN"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08."
      }
    },
    {
      "step_id": "p_x_min",
      "expression": "p_{-}=\\frac{N}{A}+\\gamma_{mt}d-\\frac{M}{W}",
      "substitutions": [
        {
          "value": 600.0,
          "unit": "kN",
          "symbol": "N"
        },
        {
          "value": 6.0,
          "unit": "m2",
          "symbol": "A"
        },
        {
          "value": 20.0,
          "unit": "kN/m3",
          "symbol": "gamma_mt"
        },
        {
          "value": 1.0,
          "unit": "m",
          "symbol": "d"
        },
        {
          "value": 180.0,
          "unit": "kN*m",
          "symbol": "M"
        },
        {
          "value": 2.0,
          "unit": "m3",
          "symbol": "W"
        }
      ],
      "result": {
        "value": 30.0,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.28, formula (5.11)",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "step_id": "p_x_max",
      "expression": "p_{+}=\\frac{N}{A}+\\gamma_{mt}d+\\frac{M}{W}",
      "substitutions": [
        {
          "value": 600.0,
          "unit": "kN",
          "symbol": "N"
        },
        {
          "value": 6.0,
          "unit": "m2",
          "symbol": "A"
        },
        {
          "value": 20.0,
          "unit": "kN/m3",
          "symbol": "gamma_mt"
        },
        {
          "value": 1.0,
          "unit": "m",
          "symbol": "d"
        },
        {
          "value": 180.0,
          "unit": "kN*m",
          "symbol": "M"
        },
        {
          "value": 2.0,
          "unit": "m3",
          "symbol": "W"
        }
      ],
      "result": {
        "value": 210.0,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.28, formula (5.11)",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "kind": "engineer_formula",
      "step_id": "e_x",
      "expression": "e_x=|M_{x,base}|/V",
      "substitutions": [
        {
          "value": 180.0,
          "unit": "kN*m",
          "symbol": "Mx_base"
        },
        {
          "value": 720.0,
          "unit": "kN",
          "symbol": "V"
        }
      ],
      "result": {
        "value": 0.25,
        "unit": "m"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08."
      }
    },
    {
      "step_id": "relative_eccentricity_x",
      "expression": "e/l\\leq1/6",
      "substitutions": [
        {
          "value": 0.125,
          "unit": "1",
          "symbol": "e/L"
        },
        {
          "value": 1.0,
          "unit": "1",
          "symbol": "numerator"
        },
        {
          "value": 6.0,
          "unit": "1",
          "symbol": "denominator"
        }
      ],
      "result": {
        "value": 1.0,
        "unit": "1"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.28, applicability of formula (5.11)",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "step_id": "pressure_diagram_x",
      "expression": "e<l/6",
      "substitutions": [
        {
          "value": 0.25,
          "unit": "m",
          "symbol": "e"
        },
        {
          "value": 2.0,
          "unit": "m",
          "symbol": "l"
        }
      ],
      "result": {
        "value": 0.25,
        "unit": "m"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.27, figure 5.1",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "step_id": "p_y_min",
      "expression": "p_{-}=\\frac{N}{A}+\\gamma_{mt}d-\\frac{M}{W}",
      "substitutions": [
        {
          "value": 600.0,
          "unit": "kN",
          "symbol": "N"
        },
        {
          "value": 6.0,
          "unit": "m2",
          "symbol": "A"
        },
        {
          "value": 20.0,
          "unit": "kN/m3",
          "symbol": "gamma_mt"
        },
        {
          "value": 1.0,
          "unit": "m",
          "symbol": "d"
        },
        {
          "value": 180.0,
          "unit": "kN*m",
          "symbol": "M"
        },
        {
          "value": 3.0,
          "unit": "m3",
          "symbol": "W"
        }
      ],
      "result": {
        "value": 60.0,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.28, formula (5.11)",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "step_id": "p_y_max",
      "expression": "p_{+}=\\frac{N}{A}+\\gamma_{mt}d+\\frac{M}{W}",
      "substitutions": [
        {
          "value": 600.0,
          "unit": "kN",
          "symbol": "N"
        },
        {
          "value": 6.0,
          "unit": "m2",
          "symbol": "A"
        },
        {
          "value": 20.0,
          "unit": "kN/m3",
          "symbol": "gamma_mt"
        },
        {
          "value": 1.0,
          "unit": "m",
          "symbol": "d"
        },
        {
          "value": 180.0,
          "unit": "kN*m",
          "symbol": "M"
        },
        {
          "value": 3.0,
          "unit": "m3",
          "symbol": "W"
        }
      ],
      "result": {
        "value": 180.0,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.28, formula (5.11)",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "kind": "engineer_formula",
      "step_id": "e_y",
      "expression": "e_y=|M_{y,base}|/V",
      "substitutions": [
        {
          "value": 180.0,
          "unit": "kN*m",
          "symbol": "My_base"
        },
        {
          "value": 720.0,
          "unit": "kN",
          "symbol": "V"
        }
      ],
      "result": {
        "value": 0.25,
        "unit": "m"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08."
      }
    },
    {
      "step_id": "relative_eccentricity_y",
      "expression": "e/l\\leq1/6",
      "substitutions": [
        {
          "value": 0.08333333333333333,
          "unit": "1",
          "symbol": "e/L"
        },
        {
          "value": 1.0,
          "unit": "1",
          "symbol": "numerator"
        },
        {
          "value": 6.0,
          "unit": "1",
          "symbol": "denominator"
        }
      ],
      "result": {
        "value": 1.0,
        "unit": "1"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.28, applicability of formula (5.11)",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "step_id": "pressure_diagram_y",
      "expression": "e<l/6",
      "substitutions": [
        {
          "value": 0.25,
          "unit": "m",
          "symbol": "e"
        },
        {
          "value": 3.0,
          "unit": "m",
          "symbol": "l"
        }
      ],
      "result": {
        "value": 0.25,
        "unit": "m"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.27, figure 5.1",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "step_id": "corner_component_pp",
      "expression": "P_{\\max}=\\frac{N}{A}+\\gamma_{mt}d+\\frac{M_x}{W_x}+\\frac{M_y}{W_y}",
      "substitutions": [
        {
          "value": 600.0,
          "unit": "kN",
          "symbol": "N"
        },
        {
          "value": 6.0,
          "unit": "m2",
          "symbol": "A"
        },
        {
          "value": 20.0,
          "unit": "kN/m3",
          "symbol": "gamma_mt"
        },
        {
          "value": 1.0,
          "unit": "m",
          "symbol": "d"
        },
        {
          "value": 180.0,
          "unit": "kN*m",
          "symbol": "M_x"
        },
        {
          "value": 2.0,
          "unit": "m3",
          "symbol": "W_x"
        },
        {
          "value": 180.0,
          "unit": "kN*m",
          "symbol": "M_y"
        },
        {
          "value": 3.0,
          "unit": "m3",
          "symbol": "W_y"
        }
      ],
      "result": {
        "value": 270.0,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.29, formula (5.15)",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "kind": "engineer_formula",
      "step_id": "p_corner_pp",
      "expression": "p_{pp}=p+s_x M_{x,base}/W_x+s_y M_{y,base}/W_y",
      "substitutions": [
        {
          "value": 120.0,
          "unit": "kPa",
          "symbol": "p"
        },
        {
          "value": 180.0,
          "unit": "kN*m",
          "symbol": "Mx_base"
        },
        {
          "value": 2.0,
          "unit": "m3",
          "symbol": "Wx"
        },
        {
          "value": 180.0,
          "unit": "kN*m",
          "symbol": "My_base"
        },
        {
          "value": 3.0,
          "unit": "m3",
          "symbol": "Wy"
        },
        {
          "value": 1.0,
          "unit": "1",
          "symbol": "sign_x_pp"
        },
        {
          "value": 1.0,
          "unit": "1",
          "symbol": "sign_y_pp"
        },
        {
          "value": 270.0,
          "unit": "kPa",
          "symbol": "corner_component_pp"
        }
      ],
      "result": {
        "value": 270.0,
        "unit": "kPa"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08."
      }
    },
    {
      "step_id": "corner_component_pm",
      "expression": "P_{\\max}=\\frac{N}{A}+\\gamma_{mt}d+\\frac{M_x}{W_x}+\\frac{M_y}{W_y}",
      "substitutions": [
        {
          "value": 600.0,
          "unit": "kN",
          "symbol": "N"
        },
        {
          "value": 6.0,
          "unit": "m2",
          "symbol": "A"
        },
        {
          "value": 20.0,
          "unit": "kN/m3",
          "symbol": "gamma_mt"
        },
        {
          "value": 1.0,
          "unit": "m",
          "symbol": "d"
        },
        {
          "value": 180.0,
          "unit": "kN*m",
          "symbol": "M_x"
        },
        {
          "value": 2.0,
          "unit": "m3",
          "symbol": "W_x"
        },
        {
          "value": -180.0,
          "unit": "kN*m",
          "symbol": "M_y"
        },
        {
          "value": 3.0,
          "unit": "m3",
          "symbol": "W_y"
        }
      ],
      "result": {
        "value": 150.0,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.29, formula (5.15)",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "kind": "engineer_formula",
      "step_id": "p_corner_pm",
      "expression": "p_{pm}=p+s_x M_{x,base}/W_x+s_y M_{y,base}/W_y",
      "substitutions": [
        {
          "value": 120.0,
          "unit": "kPa",
          "symbol": "p"
        },
        {
          "value": 180.0,
          "unit": "kN*m",
          "symbol": "Mx_base"
        },
        {
          "value": 2.0,
          "unit": "m3",
          "symbol": "Wx"
        },
        {
          "value": 180.0,
          "unit": "kN*m",
          "symbol": "My_base"
        },
        {
          "value": 3.0,
          "unit": "m3",
          "symbol": "Wy"
        },
        {
          "value": 1.0,
          "unit": "1",
          "symbol": "sign_x_pm"
        },
        {
          "value": -1.0,
          "unit": "1",
          "symbol": "sign_y_pm"
        },
        {
          "value": 150.0,
          "unit": "kPa",
          "symbol": "corner_component_pm"
        }
      ],
      "result": {
        "value": 150.0,
        "unit": "kPa"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08."
      }
    },
    {
      "step_id": "corner_component_mp",
      "expression": "P_{\\max}=\\frac{N}{A}+\\gamma_{mt}d+\\frac{M_x}{W_x}+\\frac{M_y}{W_y}",
      "substitutions": [
        {
          "value": 600.0,
          "unit": "kN",
          "symbol": "N"
        },
        {
          "value": 6.0,
          "unit": "m2",
          "symbol": "A"
        },
        {
          "value": 20.0,
          "unit": "kN/m3",
          "symbol": "gamma_mt"
        },
        {
          "value": 1.0,
          "unit": "m",
          "symbol": "d"
        },
        {
          "value": -180.0,
          "unit": "kN*m",
          "symbol": "M_x"
        },
        {
          "value": 2.0,
          "unit": "m3",
          "symbol": "W_x"
        },
        {
          "value": 180.0,
          "unit": "kN*m",
          "symbol": "M_y"
        },
        {
          "value": 3.0,
          "unit": "m3",
          "symbol": "W_y"
        }
      ],
      "result": {
        "value": 90.0,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.29, formula (5.15)",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "kind": "engineer_formula",
      "step_id": "p_corner_mp",
      "expression": "p_{mp}=p+s_x M_{x,base}/W_x+s_y M_{y,base}/W_y",
      "substitutions": [
        {
          "value": 120.0,
          "unit": "kPa",
          "symbol": "p"
        },
        {
          "value": 180.0,
          "unit": "kN*m",
          "symbol": "Mx_base"
        },
        {
          "value": 2.0,
          "unit": "m3",
          "symbol": "Wx"
        },
        {
          "value": 180.0,
          "unit": "kN*m",
          "symbol": "My_base"
        },
        {
          "value": 3.0,
          "unit": "m3",
          "symbol": "Wy"
        },
        {
          "value": -1.0,
          "unit": "1",
          "symbol": "sign_x_mp"
        },
        {
          "value": 1.0,
          "unit": "1",
          "symbol": "sign_y_mp"
        },
        {
          "value": 90.0,
          "unit": "kPa",
          "symbol": "corner_component_mp"
        }
      ],
      "result": {
        "value": 90.0,
        "unit": "kPa"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08."
      }
    },
    {
      "step_id": "corner_component_mm",
      "expression": "P_{\\max}=\\frac{N}{A}+\\gamma_{mt}d+\\frac{M_x}{W_x}+\\frac{M_y}{W_y}",
      "substitutions": [
        {
          "value": 600.0,
          "unit": "kN",
          "symbol": "N"
        },
        {
          "value": 6.0,
          "unit": "m2",
          "symbol": "A"
        },
        {
          "value": 20.0,
          "unit": "kN/m3",
          "symbol": "gamma_mt"
        },
        {
          "value": 1.0,
          "unit": "m",
          "symbol": "d"
        },
        {
          "value": -180.0,
          "unit": "kN*m",
          "symbol": "M_x"
        },
        {
          "value": 2.0,
          "unit": "m3",
          "symbol": "W_x"
        },
        {
          "value": -180.0,
          "unit": "kN*m",
          "symbol": "M_y"
        },
        {
          "value": 3.0,
          "unit": "m3",
          "symbol": "W_y"
        }
      ],
      "result": {
        "value": -30.0,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.29, formula (5.15)",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "kind": "engineer_formula",
      "step_id": "p_corner_mm",
      "expression": "p_{mm}=p+s_x M_{x,base}/W_x+s_y M_{y,base}/W_y",
      "substitutions": [
        {
          "value": 120.0,
          "unit": "kPa",
          "symbol": "p"
        },
        {
          "value": 180.0,
          "unit": "kN*m",
          "symbol": "Mx_base"
        },
        {
          "value": 2.0,
          "unit": "m3",
          "symbol": "Wx"
        },
        {
          "value": 180.0,
          "unit": "kN*m",
          "symbol": "My_base"
        },
        {
          "value": 3.0,
          "unit": "m3",
          "symbol": "Wy"
        },
        {
          "value": -1.0,
          "unit": "1",
          "symbol": "sign_x_mm"
        },
        {
          "value": -1.0,
          "unit": "1",
          "symbol": "sign_y_mm"
        },
        {
          "value": -30.0,
          "unit": "kPa",
          "symbol": "corner_component_mm"
        }
      ],
      "result": {
        "value": -30.0,
        "unit": "kPa"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08."
      }
    },
    {
      "kind": "engineer_formula",
      "step_id": "p_corner_min",
      "expression": "p_{corner,min}=\\min(p_{++},p_{+-},p_{-+},p_{--})",
      "substitutions": [
        {
          "value": 270.0,
          "unit": "kPa",
          "symbol": "p_corner_pp"
        },
        {
          "value": 150.0,
          "unit": "kPa",
          "symbol": "p_corner_pm"
        },
        {
          "value": 90.0,
          "unit": "kPa",
          "symbol": "p_corner_mp"
        },
        {
          "value": -30.0,
          "unit": "kPa",
          "symbol": "p_corner_mm"
        }
      ],
      "result": {
        "value": -30.0,
        "unit": "kPa"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Полный контакт прямоугольной подошвы: минимум четырёх подписанных угловых давлений неотрицателен; решение инженера 2026-11-08."
      }
    },
    {
      "kind": "engineer_formula",
      "step_id": "p_corner_max",
      "expression": "p_{corner,max}=\\max(p_{++},p_{+-},p_{-+},p_{--})",
      "substitutions": [
        {
          "value": 270.0,
          "unit": "kPa",
          "symbol": "p_corner_pp"
        },
        {
          "value": 150.0,
          "unit": "kPa",
          "symbol": "p_corner_pm"
        },
        {
          "value": 90.0,
          "unit": "kPa",
          "symbol": "p_corner_mp"
        },
        {
          "value": -30.0,
          "unit": "kPa",
          "symbol": "p_corner_mm"
        }
      ],
      "result": {
        "value": 270.0,
        "unit": "kPa"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08."
      }
    }
  ],
  "unverified_step_count": 22,
  "result_id": "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa",
  "parameter_source": {
    "kind": "interim",
    "data_sha256": "faaa0724af57ca6c8066f558c4e75c2785d099b34cbfb07c4a85892fdc3b68fe", // pragma: allowlist secret
    "profile": "strict"
  }
} satisfies ResultEnvelope

export const loadsContactRefusalJson = "{\"engine_version\":\"0.1.0\",\"input_hash\":\"f4b13a8543416777e9a56a89b3e498631219a7ef77ceff19a3a9b5da628076b5\",\"outputs\":[],\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7, таблица 5.4\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"},{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7, экспликация k\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"},{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7, таблица 5.5\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"},{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7, экспликация k_z\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"},{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7, формула (5.7)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"},{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.28, explanation of formula (5.11)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"},{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.28, formula (5.11)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"},{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.28, applicability of formula (5.11)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"},{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.27, figure 5.1\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"},{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.29, formula (5.15)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"engineer_rules\":[{\"engineer\":\"Аким\",\"rationale\":\"Геометрия прямоугольной подошвы: A=b*l, Wx=l*b²/6, Wy=b*l²/6; инженерный контракт 2026-11-08.\"},{\"engineer\":\"Аким\",\"rationale\":\"Подписанный перенос нагрузок к подошве M_base=M+Q*h; оси x=b и y=l; инженерный контракт 2026-11-08.\"},{\"engineer\":\"Аким\",\"rationale\":\"Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08.\"},{\"engineer\":\"Аким\",\"rationale\":\"Полный контакт прямоугольной подошвы: минимум четырёх подписанных угловых давлений неотрицателен; решение инженера 2026-11-08.\"}],\"verdict\":\"refused\",\"verdict_reason\":{\"kind\":\"derived\",\"check_id\":\"full_contact\",\"step_id\":\"p_corner_min\",\"quantity\":\"p_corner_min\",\"value\":{\"value\":-30.0,\"unit\":\"kPa\"},\"operator\":\"ge\",\"limit\":{\"value\":0.0,\"unit\":\"kPa\"},\"source\":{\"engineer\":\"Аким\",\"rationale\":\"Полный контакт прямоугольной подошвы: минимум четырёх подписанных угловых давлений неотрицателен; решение инженера 2026-11-08.\"},\"related_inputs\":[\"N\",\"Mx\",\"My\",\"Qx\",\"Qy\",\"h\",\"b\",\"l\",\"d\"],\"limiting_corner\":\"mm\"},\"warnings\":[],\"trace\":[{\"step_id\":\"gamma_c1\",\"expression\":\"\\\\gamma_{c1}\",\"substitutions\":[],\"result\":{\"value\":1.1,\"unit\":\"1\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7, таблица 5.4\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"table\"},{\"step_id\":\"gamma_c2\",\"expression\":\"\\\\gamma_{c2}\",\"substitutions\":[],\"result\":{\"value\":1.0,\"unit\":\"1\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7, таблица 5.4\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"table\"},{\"step_id\":\"k\",\"expression\":\"k\",\"substitutions\":[],\"result\":{\"value\":1.0,\"unit\":\"1\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7, экспликация k\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"table\"},{\"step_id\":\"M_gamma\",\"expression\":\"M_{\\\\gamma} = M_{\\\\gamma}\\\\left(\\\\varphi_{II}\\\\right)\",\"substitutions\":[{\"value\":20.0,\"unit\":\"deg\",\"symbol\":\"phi_II\"}],\"result\":{\"value\":0.51,\"unit\":\"1\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7, таблица 5.5\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"table\"},{\"step_id\":\"M_q\",\"expression\":\"M_{q} = M_{q}\\\\left(\\\\varphi_{II}\\\\right)\",\"substitutions\":[{\"value\":20.0,\"unit\":\"deg\",\"symbol\":\"phi_II\"}],\"result\":{\"value\":3.06,\"unit\":\"1\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7, таблица 5.5\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"table\"},{\"step_id\":\"M_c\",\"expression\":\"M_{c} = M_{c}\\\\left(\\\\varphi_{II}\\\\right)\",\"substitutions\":[{\"value\":20.0,\"unit\":\"deg\",\"symbol\":\"phi_II\"}],\"result\":{\"value\":5.66,\"unit\":\"1\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7, таблица 5.5\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"table\"},{\"step_id\":\"k_z\",\"expression\":\"k_{z}=1\",\"substitutions\":[],\"result\":{\"value\":1.0,\"unit\":\"1\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7, экспликация k_z\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"step_id\":\"R\",\"expression\":\"R=\\\\frac{\\\\gamma_{c1}\\\\gamma_{c2}}{k}\\\\left[M_{\\\\gamma}k_{z}b\\\\gamma_{II}+M_{q}d_{1}\\\\gamma'_{II}+(M_{q}-1)d_{b}\\\\gamma'_{II}+M_{c}c_{II}\\\\right]\",\"substitutions\":[{\"value\":1.1,\"unit\":\"1\",\"symbol\":\"gamma_c1\"},{\"value\":1.0,\"unit\":\"1\",\"symbol\":\"gamma_c2\"},{\"value\":1.0,\"unit\":\"1\",\"symbol\":\"k\"},{\"value\":0.51,\"unit\":\"1\",\"symbol\":\"M_gamma\"},{\"value\":1.0,\"unit\":\"1\",\"symbol\":\"k_z\"},{\"value\":2.0,\"unit\":\"m\",\"symbol\":\"b\"},{\"value\":20.0,\"unit\":\"kN/m3\",\"symbol\":\"gamma_II\"},{\"value\":3.06,\"unit\":\"1\",\"symbol\":\"M_q\"},{\"value\":1.0,\"unit\":\"m\",\"symbol\":\"d_1\"},{\"value\":20.0,\"unit\":\"kN/m3\",\"symbol\":\"gamma_II_prime\"},{\"value\":0.0,\"unit\":\"m\",\"symbol\":\"d_b\"},{\"value\":5.66,\"unit\":\"1\",\"symbol\":\"M_c\"},{\"value\":10.0,\"unit\":\"kPa\",\"symbol\":\"c_II\"}],\"result\":{\"value\":152.02,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7, формула (5.7)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"kind\":\"engineer_formula\",\"step_id\":\"A\",\"expression\":\"A=b l\",\"substitutions\":[{\"value\":2.0,\"unit\":\"m\",\"symbol\":\"b\"},{\"value\":3.0,\"unit\":\"m\",\"symbol\":\"l\"}],\"result\":{\"value\":6.0,\"unit\":\"m2\"},\"source\":{\"engineer\":\"Аким\",\"rationale\":\"Геометрия прямоугольной подошвы: A=b*l, Wx=l*b²/6, Wy=b*l²/6; инженерный контракт 2026-11-08.\"}},{\"kind\":\"engineer_formula\",\"step_id\":\"Wx\",\"expression\":\"W_x=l b^2/6\",\"substitutions\":[{\"value\":2.0,\"unit\":\"m\",\"symbol\":\"b\"},{\"value\":3.0,\"unit\":\"m\",\"symbol\":\"l\"}],\"result\":{\"value\":2.0,\"unit\":\"m3\"},\"source\":{\"engineer\":\"Аким\",\"rationale\":\"Геометрия прямоугольной подошвы: A=b*l, Wx=l*b²/6, Wy=b*l²/6; инженерный контракт 2026-11-08.\"}},{\"kind\":\"engineer_formula\",\"step_id\":\"Wy\",\"expression\":\"W_y=b l^2/6\",\"substitutions\":[{\"value\":2.0,\"unit\":\"m\",\"symbol\":\"b\"},{\"value\":3.0,\"unit\":\"m\",\"symbol\":\"l\"}],\"result\":{\"value\":3.0,\"unit\":\"m3\"},\"source\":{\"engineer\":\"Аким\",\"rationale\":\"Геометрия прямоугольной подошвы: A=b*l, Wx=l*b²/6, Wy=b*l²/6; инженерный контракт 2026-11-08.\"}},{\"kind\":\"engineer_formula\",\"step_id\":\"Mx_base\",\"expression\":\"M_{x,base}=M_x+Q_x h\",\"substitutions\":[{\"value\":180.0,\"unit\":\"kN*m\",\"symbol\":\"Mx\"},{\"value\":0.0,\"unit\":\"kN\",\"symbol\":\"Qx\"},{\"value\":1.0,\"unit\":\"m\",\"symbol\":\"h\"}],\"result\":{\"value\":180.0,\"unit\":\"kN*m\"},\"source\":{\"engineer\":\"Аким\",\"rationale\":\"Подписанный перенос нагрузок к подошве M_base=M+Q*h; оси x=b и y=l; инженерный контракт 2026-11-08.\"}},{\"kind\":\"engineer_formula\",\"step_id\":\"My_base\",\"expression\":\"M_{y,base}=M_y+Q_y h\",\"substitutions\":[{\"value\":180.0,\"unit\":\"kN*m\",\"symbol\":\"My\"},{\"value\":0.0,\"unit\":\"kN\",\"symbol\":\"Qy\"},{\"value\":1.0,\"unit\":\"m\",\"symbol\":\"h\"}],\"result\":{\"value\":180.0,\"unit\":\"kN*m\"},\"source\":{\"engineer\":\"Аким\",\"rationale\":\"Подписанный перенос нагрузок к подошве M_base=M+Q*h; оси x=b и y=l; инженерный контракт 2026-11-08.\"}},{\"step_id\":\"gamma_mt\",\"expression\":\"\\\\gamma_{mt}\",\"substitutions\":[],\"result\":{\"value\":20.0,\"unit\":\"kN/m3\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.28, explanation of formula (5.11)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"table\"},{\"step_id\":\"p\",\"expression\":\"p_{+}=\\\\frac{N}{A}+\\\\gamma_{mt}d+\\\\frac{M}{W}\",\"substitutions\":[{\"value\":600.0,\"unit\":\"kN\",\"symbol\":\"N\"},{\"value\":6.0,\"unit\":\"m2\",\"symbol\":\"A\"},{\"value\":20.0,\"unit\":\"kN/m3\",\"symbol\":\"gamma_mt\"},{\"value\":1.0,\"unit\":\"m\",\"symbol\":\"d\"},{\"value\":0.0,\"unit\":\"kN*m\",\"symbol\":\"M\"},{\"value\":2.0,\"unit\":\"m3\",\"symbol\":\"W\"}],\"result\":{\"value\":120.0,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.28, formula (5.11)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"kind\":\"engineer_formula\",\"step_id\":\"V\",\"expression\":\"V=N+\\\\gamma_{mt} d A\",\"substitutions\":[{\"value\":600.0,\"unit\":\"kN\",\"symbol\":\"N\"},{\"value\":20.0,\"unit\":\"kN/m3\",\"symbol\":\"gamma_mt\"},{\"value\":1.0,\"unit\":\"m\",\"symbol\":\"d\"},{\"value\":6.0,\"unit\":\"m2\",\"symbol\":\"A\"}],\"result\":{\"value\":720.0,\"unit\":\"kN\"},\"source\":{\"engineer\":\"Аким\",\"rationale\":\"Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08.\"}},{\"step_id\":\"p_x_min\",\"expression\":\"p_{-}=\\\\frac{N}{A}+\\\\gamma_{mt}d-\\\\frac{M}{W}\",\"substitutions\":[{\"value\":600.0,\"unit\":\"kN\",\"symbol\":\"N\"},{\"value\":6.0,\"unit\":\"m2\",\"symbol\":\"A\"},{\"value\":20.0,\"unit\":\"kN/m3\",\"symbol\":\"gamma_mt\"},{\"value\":1.0,\"unit\":\"m\",\"symbol\":\"d\"},{\"value\":180.0,\"unit\":\"kN*m\",\"symbol\":\"M\"},{\"value\":2.0,\"unit\":\"m3\",\"symbol\":\"W\"}],\"result\":{\"value\":30.0,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.28, formula (5.11)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"step_id\":\"p_x_max\",\"expression\":\"p_{+}=\\\\frac{N}{A}+\\\\gamma_{mt}d+\\\\frac{M}{W}\",\"substitutions\":[{\"value\":600.0,\"unit\":\"kN\",\"symbol\":\"N\"},{\"value\":6.0,\"unit\":\"m2\",\"symbol\":\"A\"},{\"value\":20.0,\"unit\":\"kN/m3\",\"symbol\":\"gamma_mt\"},{\"value\":1.0,\"unit\":\"m\",\"symbol\":\"d\"},{\"value\":180.0,\"unit\":\"kN*m\",\"symbol\":\"M\"},{\"value\":2.0,\"unit\":\"m3\",\"symbol\":\"W\"}],\"result\":{\"value\":210.0,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.28, formula (5.11)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"kind\":\"engineer_formula\",\"step_id\":\"e_x\",\"expression\":\"e_x=|M_{x,base}|/V\",\"substitutions\":[{\"value\":180.0,\"unit\":\"kN*m\",\"symbol\":\"Mx_base\"},{\"value\":720.0,\"unit\":\"kN\",\"symbol\":\"V\"}],\"result\":{\"value\":0.25,\"unit\":\"m\"},\"source\":{\"engineer\":\"Аким\",\"rationale\":\"Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08.\"}},{\"step_id\":\"relative_eccentricity_x\",\"expression\":\"e/l\\\\leq1/6\",\"substitutions\":[{\"value\":0.125,\"unit\":\"1\",\"symbol\":\"e/L\"},{\"value\":1.0,\"unit\":\"1\",\"symbol\":\"numerator\"},{\"value\":6.0,\"unit\":\"1\",\"symbol\":\"denominator\"}],\"result\":{\"value\":1.0,\"unit\":\"1\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.28, applicability of formula (5.11)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"step_id\":\"pressure_diagram_x\",\"expression\":\"e<l/6\",\"substitutions\":[{\"value\":0.25,\"unit\":\"m\",\"symbol\":\"e\"},{\"value\":2.0,\"unit\":\"m\",\"symbol\":\"l\"}],\"result\":{\"value\":0.25,\"unit\":\"m\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.27, figure 5.1\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"step_id\":\"p_y_min\",\"expression\":\"p_{-}=\\\\frac{N}{A}+\\\\gamma_{mt}d-\\\\frac{M}{W}\",\"substitutions\":[{\"value\":600.0,\"unit\":\"kN\",\"symbol\":\"N\"},{\"value\":6.0,\"unit\":\"m2\",\"symbol\":\"A\"},{\"value\":20.0,\"unit\":\"kN/m3\",\"symbol\":\"gamma_mt\"},{\"value\":1.0,\"unit\":\"m\",\"symbol\":\"d\"},{\"value\":180.0,\"unit\":\"kN*m\",\"symbol\":\"M\"},{\"value\":3.0,\"unit\":\"m3\",\"symbol\":\"W\"}],\"result\":{\"value\":60.0,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.28, formula (5.11)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"step_id\":\"p_y_max\",\"expression\":\"p_{+}=\\\\frac{N}{A}+\\\\gamma_{mt}d+\\\\frac{M}{W}\",\"substitutions\":[{\"value\":600.0,\"unit\":\"kN\",\"symbol\":\"N\"},{\"value\":6.0,\"unit\":\"m2\",\"symbol\":\"A\"},{\"value\":20.0,\"unit\":\"kN/m3\",\"symbol\":\"gamma_mt\"},{\"value\":1.0,\"unit\":\"m\",\"symbol\":\"d\"},{\"value\":180.0,\"unit\":\"kN*m\",\"symbol\":\"M\"},{\"value\":3.0,\"unit\":\"m3\",\"symbol\":\"W\"}],\"result\":{\"value\":180.0,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.28, formula (5.11)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"kind\":\"engineer_formula\",\"step_id\":\"e_y\",\"expression\":\"e_y=|M_{y,base}|/V\",\"substitutions\":[{\"value\":180.0,\"unit\":\"kN*m\",\"symbol\":\"My_base\"},{\"value\":720.0,\"unit\":\"kN\",\"symbol\":\"V\"}],\"result\":{\"value\":0.25,\"unit\":\"m\"},\"source\":{\"engineer\":\"Аким\",\"rationale\":\"Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08.\"}},{\"step_id\":\"relative_eccentricity_y\",\"expression\":\"e/l\\\\leq1/6\",\"substitutions\":[{\"value\":0.08333333333333333,\"unit\":\"1\",\"symbol\":\"e/L\"},{\"value\":1.0,\"unit\":\"1\",\"symbol\":\"numerator\"},{\"value\":6.0,\"unit\":\"1\",\"symbol\":\"denominator\"}],\"result\":{\"value\":1.0,\"unit\":\"1\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.28, applicability of formula (5.11)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"step_id\":\"pressure_diagram_y\",\"expression\":\"e<l/6\",\"substitutions\":[{\"value\":0.25,\"unit\":\"m\",\"symbol\":\"e\"},{\"value\":3.0,\"unit\":\"m\",\"symbol\":\"l\"}],\"result\":{\"value\":0.25,\"unit\":\"m\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.27, figure 5.1\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"step_id\":\"corner_component_pp\",\"expression\":\"P_{\\\\max}=\\\\frac{N}{A}+\\\\gamma_{mt}d+\\\\frac{M_x}{W_x}+\\\\frac{M_y}{W_y}\",\"substitutions\":[{\"value\":600.0,\"unit\":\"kN\",\"symbol\":\"N\"},{\"value\":6.0,\"unit\":\"m2\",\"symbol\":\"A\"},{\"value\":20.0,\"unit\":\"kN/m3\",\"symbol\":\"gamma_mt\"},{\"value\":1.0,\"unit\":\"m\",\"symbol\":\"d\"},{\"value\":180.0,\"unit\":\"kN*m\",\"symbol\":\"M_x\"},{\"value\":2.0,\"unit\":\"m3\",\"symbol\":\"W_x\"},{\"value\":180.0,\"unit\":\"kN*m\",\"symbol\":\"M_y\"},{\"value\":3.0,\"unit\":\"m3\",\"symbol\":\"W_y\"}],\"result\":{\"value\":270.0,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.29, formula (5.15)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"kind\":\"engineer_formula\",\"step_id\":\"p_corner_pp\",\"expression\":\"p_{pp}=p+s_x M_{x,base}/W_x+s_y M_{y,base}/W_y\",\"substitutions\":[{\"value\":120.0,\"unit\":\"kPa\",\"symbol\":\"p\"},{\"value\":180.0,\"unit\":\"kN*m\",\"symbol\":\"Mx_base\"},{\"value\":2.0,\"unit\":\"m3\",\"symbol\":\"Wx\"},{\"value\":180.0,\"unit\":\"kN*m\",\"symbol\":\"My_base\"},{\"value\":3.0,\"unit\":\"m3\",\"symbol\":\"Wy\"},{\"value\":1.0,\"unit\":\"1\",\"symbol\":\"sign_x_pp\"},{\"value\":1.0,\"unit\":\"1\",\"symbol\":\"sign_y_pp\"},{\"value\":270.0,\"unit\":\"kPa\",\"symbol\":\"corner_component_pp\"}],\"result\":{\"value\":270.0,\"unit\":\"kPa\"},\"source\":{\"engineer\":\"Аким\",\"rationale\":\"Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08.\"}},{\"step_id\":\"corner_component_pm\",\"expression\":\"P_{\\\\max}=\\\\frac{N}{A}+\\\\gamma_{mt}d+\\\\frac{M_x}{W_x}+\\\\frac{M_y}{W_y}\",\"substitutions\":[{\"value\":600.0,\"unit\":\"kN\",\"symbol\":\"N\"},{\"value\":6.0,\"unit\":\"m2\",\"symbol\":\"A\"},{\"value\":20.0,\"unit\":\"kN/m3\",\"symbol\":\"gamma_mt\"},{\"value\":1.0,\"unit\":\"m\",\"symbol\":\"d\"},{\"value\":180.0,\"unit\":\"kN*m\",\"symbol\":\"M_x\"},{\"value\":2.0,\"unit\":\"m3\",\"symbol\":\"W_x\"},{\"value\":-180.0,\"unit\":\"kN*m\",\"symbol\":\"M_y\"},{\"value\":3.0,\"unit\":\"m3\",\"symbol\":\"W_y\"}],\"result\":{\"value\":150.0,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.29, formula (5.15)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"kind\":\"engineer_formula\",\"step_id\":\"p_corner_pm\",\"expression\":\"p_{pm}=p+s_x M_{x,base}/W_x+s_y M_{y,base}/W_y\",\"substitutions\":[{\"value\":120.0,\"unit\":\"kPa\",\"symbol\":\"p\"},{\"value\":180.0,\"unit\":\"kN*m\",\"symbol\":\"Mx_base\"},{\"value\":2.0,\"unit\":\"m3\",\"symbol\":\"Wx\"},{\"value\":180.0,\"unit\":\"kN*m\",\"symbol\":\"My_base\"},{\"value\":3.0,\"unit\":\"m3\",\"symbol\":\"Wy\"},{\"value\":1.0,\"unit\":\"1\",\"symbol\":\"sign_x_pm\"},{\"value\":-1.0,\"unit\":\"1\",\"symbol\":\"sign_y_pm\"},{\"value\":150.0,\"unit\":\"kPa\",\"symbol\":\"corner_component_pm\"}],\"result\":{\"value\":150.0,\"unit\":\"kPa\"},\"source\":{\"engineer\":\"Аким\",\"rationale\":\"Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08.\"}},{\"step_id\":\"corner_component_mp\",\"expression\":\"P_{\\\\max}=\\\\frac{N}{A}+\\\\gamma_{mt}d+\\\\frac{M_x}{W_x}+\\\\frac{M_y}{W_y}\",\"substitutions\":[{\"value\":600.0,\"unit\":\"kN\",\"symbol\":\"N\"},{\"value\":6.0,\"unit\":\"m2\",\"symbol\":\"A\"},{\"value\":20.0,\"unit\":\"kN/m3\",\"symbol\":\"gamma_mt\"},{\"value\":1.0,\"unit\":\"m\",\"symbol\":\"d\"},{\"value\":-180.0,\"unit\":\"kN*m\",\"symbol\":\"M_x\"},{\"value\":2.0,\"unit\":\"m3\",\"symbol\":\"W_x\"},{\"value\":180.0,\"unit\":\"kN*m\",\"symbol\":\"M_y\"},{\"value\":3.0,\"unit\":\"m3\",\"symbol\":\"W_y\"}],\"result\":{\"value\":90.0,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.29, formula (5.15)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"kind\":\"engineer_formula\",\"step_id\":\"p_corner_mp\",\"expression\":\"p_{mp}=p+s_x M_{x,base}/W_x+s_y M_{y,base}/W_y\",\"substitutions\":[{\"value\":120.0,\"unit\":\"kPa\",\"symbol\":\"p\"},{\"value\":180.0,\"unit\":\"kN*m\",\"symbol\":\"Mx_base\"},{\"value\":2.0,\"unit\":\"m3\",\"symbol\":\"Wx\"},{\"value\":180.0,\"unit\":\"kN*m\",\"symbol\":\"My_base\"},{\"value\":3.0,\"unit\":\"m3\",\"symbol\":\"Wy\"},{\"value\":-1.0,\"unit\":\"1\",\"symbol\":\"sign_x_mp\"},{\"value\":1.0,\"unit\":\"1\",\"symbol\":\"sign_y_mp\"},{\"value\":90.0,\"unit\":\"kPa\",\"symbol\":\"corner_component_mp\"}],\"result\":{\"value\":90.0,\"unit\":\"kPa\"},\"source\":{\"engineer\":\"Аким\",\"rationale\":\"Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08.\"}},{\"step_id\":\"corner_component_mm\",\"expression\":\"P_{\\\\max}=\\\\frac{N}{A}+\\\\gamma_{mt}d+\\\\frac{M_x}{W_x}+\\\\frac{M_y}{W_y}\",\"substitutions\":[{\"value\":600.0,\"unit\":\"kN\",\"symbol\":\"N\"},{\"value\":6.0,\"unit\":\"m2\",\"symbol\":\"A\"},{\"value\":20.0,\"unit\":\"kN/m3\",\"symbol\":\"gamma_mt\"},{\"value\":1.0,\"unit\":\"m\",\"symbol\":\"d\"},{\"value\":-180.0,\"unit\":\"kN*m\",\"symbol\":\"M_x\"},{\"value\":2.0,\"unit\":\"m3\",\"symbol\":\"W_x\"},{\"value\":-180.0,\"unit\":\"kN*m\",\"symbol\":\"M_y\"},{\"value\":3.0,\"unit\":\"m3\",\"symbol\":\"W_y\"}],\"result\":{\"value\":-30.0,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.29, formula (5.15)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"kind\":\"engineer_formula\",\"step_id\":\"p_corner_mm\",\"expression\":\"p_{mm}=p+s_x M_{x,base}/W_x+s_y M_{y,base}/W_y\",\"substitutions\":[{\"value\":120.0,\"unit\":\"kPa\",\"symbol\":\"p\"},{\"value\":180.0,\"unit\":\"kN*m\",\"symbol\":\"Mx_base\"},{\"value\":2.0,\"unit\":\"m3\",\"symbol\":\"Wx\"},{\"value\":180.0,\"unit\":\"kN*m\",\"symbol\":\"My_base\"},{\"value\":3.0,\"unit\":\"m3\",\"symbol\":\"Wy\"},{\"value\":-1.0,\"unit\":\"1\",\"symbol\":\"sign_x_mm\"},{\"value\":-1.0,\"unit\":\"1\",\"symbol\":\"sign_y_mm\"},{\"value\":-30.0,\"unit\":\"kPa\",\"symbol\":\"corner_component_mm\"}],\"result\":{\"value\":-30.0,\"unit\":\"kPa\"},\"source\":{\"engineer\":\"Аким\",\"rationale\":\"Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08.\"}},{\"kind\":\"engineer_formula\",\"step_id\":\"p_corner_min\",\"expression\":\"p_{corner,min}=\\\\min(p_{++},p_{+-},p_{-+},p_{--})\",\"substitutions\":[{\"value\":270.0,\"unit\":\"kPa\",\"symbol\":\"p_corner_pp\"},{\"value\":150.0,\"unit\":\"kPa\",\"symbol\":\"p_corner_pm\"},{\"value\":90.0,\"unit\":\"kPa\",\"symbol\":\"p_corner_mp\"},{\"value\":-30.0,\"unit\":\"kPa\",\"symbol\":\"p_corner_mm\"}],\"result\":{\"value\":-30.0,\"unit\":\"kPa\"},\"source\":{\"engineer\":\"Аким\",\"rationale\":\"Полный контакт прямоугольной подошвы: минимум четырёх подписанных угловых давлений неотрицателен; решение инженера 2026-11-08.\"}},{\"kind\":\"engineer_formula\",\"step_id\":\"p_corner_max\",\"expression\":\"p_{corner,max}=\\\\max(p_{++},p_{+-},p_{-+},p_{--})\",\"substitutions\":[{\"value\":270.0,\"unit\":\"kPa\",\"symbol\":\"p_corner_pp\"},{\"value\":150.0,\"unit\":\"kPa\",\"symbol\":\"p_corner_pm\"},{\"value\":90.0,\"unit\":\"kPa\",\"symbol\":\"p_corner_mp\"},{\"value\":-30.0,\"unit\":\"kPa\",\"symbol\":\"p_corner_mm\"}],\"result\":{\"value\":270.0,\"unit\":\"kPa\"},\"source\":{\"engineer\":\"Аким\",\"rationale\":\"Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08.\"}}],\"unverified_step_count\":22,\"result_id\":\"aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa\",\"parameter_source\":{\"kind\":\"interim\",\"data_sha256\":\"faaa0724af57ca6c8066f558c4e75c2785d099b34cbfb07c4a85892fdc3b68fe\",\"profile\":\"strict\"}}"

export const LOADS_ZERO_CONTACT_ID = 'bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb'

export const loadsZeroContactInputs = {
  "b": {
    "value": 2,
    "unit": "m"
  },
  "d_1": {
    "value": 1,
    "unit": "m"
  },
  "d_b": {
    "value": 0,
    "unit": "m"
  },
  "gamma_II": {
    "value": 20,
    "unit": "kN/m3"
  },
  "gamma_II_prime": {
    "value": 20,
    "unit": "kN/m3"
  },
  "c_II": {
    "value": 10,
    "unit": "kPa"
  },
  "phi_II": {
    "value": 20,
    "unit": "deg"
  },
  "l": {
    "value": 3,
    "unit": "m"
  },
  "h": {
    "value": 1,
    "unit": "m"
  },
  "d": {
    "value": 1,
    "unit": "m"
  },
  "N": {
    "value": 600,
    "unit": "kN"
  },
  "Mx": {
    "value": 240,
    "unit": "kN*m"
  },
  "My": {
    "value": 0,
    "unit": "kN*m"
  },
  "Qx": {
    "value": 0,
    "unit": "kN"
  },
  "Qy": {
    "value": 0,
    "unit": "kN"
  }
} satisfies CalculationRequest['inputs']

export const loadsZeroContactEnvelope = {
  "engine_version": "0.1.0",
  "input_hash": "082595b7d7fd71d3242a407044bae8c0fc4e191b35f080bb5f1b9ddd59c89dc4", // pragma: allowlist secret
  "outputs": [
    {
      "value": 152.02,
      "unit": "kPa",
      "quantity": "R",
      "rounding_rule": {
        "decimals": 2,
        "mode": "half_up"
      },
      "rounding_source": {
        "engineer": "Аким",
        "rationale": "Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются."
      }
    },
    {
      "value": 120.0,
      "unit": "kPa",
      "quantity": "p",
      "rounding_rule": {
        "decimals": 2,
        "mode": "half_up"
      },
      "rounding_source": {
        "engineer": "Аким",
        "rationale": "Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются."
      }
    },
    {
      "value": 0.0,
      "unit": "kPa",
      "quantity": "p_x_min",
      "rounding_rule": {
        "decimals": 2,
        "mode": "half_up"
      },
      "rounding_source": {
        "engineer": "Аким",
        "rationale": "Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются."
      }
    },
    {
      "value": 240.0,
      "unit": "kPa",
      "quantity": "p_x_max",
      "rounding_rule": {
        "decimals": 2,
        "mode": "half_up"
      },
      "rounding_source": {
        "engineer": "Аким",
        "rationale": "Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются."
      }
    },
    {
      "value": 120.0,
      "unit": "kPa",
      "quantity": "p_y_min",
      "rounding_rule": {
        "decimals": 2,
        "mode": "half_up"
      },
      "rounding_source": {
        "engineer": "Аким",
        "rationale": "Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются."
      }
    },
    {
      "value": 120.0,
      "unit": "kPa",
      "quantity": "p_y_max",
      "rounding_rule": {
        "decimals": 2,
        "mode": "half_up"
      },
      "rounding_source": {
        "engineer": "Аким",
        "rationale": "Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются."
      }
    },
    {
      "value": 240.0,
      "unit": "kPa",
      "quantity": "p_corner_pp",
      "rounding_rule": {
        "decimals": 2,
        "mode": "half_up"
      },
      "rounding_source": {
        "engineer": "Аким",
        "rationale": "Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются."
      }
    },
    {
      "value": 240.0,
      "unit": "kPa",
      "quantity": "p_corner_pm",
      "rounding_rule": {
        "decimals": 2,
        "mode": "half_up"
      },
      "rounding_source": {
        "engineer": "Аким",
        "rationale": "Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются."
      }
    },
    {
      "value": 0.0,
      "unit": "kPa",
      "quantity": "p_corner_mp",
      "rounding_rule": {
        "decimals": 2,
        "mode": "half_up"
      },
      "rounding_source": {
        "engineer": "Аким",
        "rationale": "Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются."
      }
    },
    {
      "value": 0.0,
      "unit": "kPa",
      "quantity": "p_corner_mm",
      "rounding_rule": {
        "decimals": 2,
        "mode": "half_up"
      },
      "rounding_source": {
        "engineer": "Аким",
        "rationale": "Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются."
      }
    }
  ],
  "norm_refs": [
    {
      "document": "СП 22.13330.2016",
      "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
      "clause": "5.6.7, таблица 5.4",
      "status": "unverified",
      "provenance": "machine-extracted"
    },
    {
      "document": "СП 22.13330.2016",
      "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
      "clause": "5.6.7, экспликация k",
      "status": "unverified",
      "provenance": "machine-extracted"
    },
    {
      "document": "СП 22.13330.2016",
      "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
      "clause": "5.6.7, таблица 5.5",
      "status": "unverified",
      "provenance": "machine-extracted"
    },
    {
      "document": "СП 22.13330.2016",
      "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
      "clause": "5.6.7, экспликация k_z",
      "status": "unverified",
      "provenance": "machine-extracted"
    },
    {
      "document": "СП 22.13330.2016",
      "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
      "clause": "5.6.7, формула (5.7)",
      "status": "unverified",
      "provenance": "machine-extracted"
    },
    {
      "document": "СП 22.13330.2016",
      "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
      "clause": "5.6.28, explanation of formula (5.11)",
      "status": "unverified",
      "provenance": "machine-extracted"
    },
    {
      "document": "СП 22.13330.2016",
      "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
      "clause": "5.6.28, formula (5.11)",
      "status": "unverified",
      "provenance": "machine-extracted"
    },
    {
      "document": "СП 22.13330.2016",
      "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
      "clause": "5.6.28, applicability of formula (5.11)",
      "status": "unverified",
      "provenance": "machine-extracted"
    },
    {
      "document": "СП 22.13330.2016",
      "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
      "clause": "5.6.27, figure 5.1",
      "status": "unverified",
      "provenance": "machine-extracted"
    },
    {
      "document": "СП 22.13330.2016",
      "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
      "clause": "5.6.29, formula (5.15)",
      "status": "unverified",
      "provenance": "machine-extracted"
    },
    {
      "document": "СП 22.13330.2016",
      "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
      "clause": "5.6.26",
      "status": "unverified",
      "provenance": "machine-extracted"
    },
    {
      "document": "СП 22.13330.2016",
      "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
      "clause": "5.6.7",
      "status": "unverified",
      "provenance": "machine-extracted"
    }
  ],
  "engineer_rules": [
    {
      "engineer": "Аким",
      "rationale": "Геометрия прямоугольной подошвы: A=b*l, Wx=l*b²/6, Wy=b*l²/6; инженерный контракт 2026-11-08."
    },
    {
      "engineer": "Аким",
      "rationale": "Подписанный перенос нагрузок к подошве M_base=M+Q*h; оси x=b и y=l; инженерный контракт 2026-11-08."
    },
    {
      "engineer": "Аким",
      "rationale": "Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08."
    },
    {
      "engineer": "Аким",
      "rationale": "Полный контакт прямоугольной подошвы: минимум четырёх подписанных угловых давлений неотрицателен; решение инженера 2026-11-08."
    },
    {
      "engineer": "Аким",
      "rationale": "Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются."
    }
  ],
  "verdict": "fail",
  "verdict_reason": {
    "kind": "check",
    "step_id": "p_x_max_le_limit"
  },
  "warnings": [],
  "trace": [
    {
      "step_id": "gamma_c1",
      "expression": "\\gamma_{c1}",
      "substitutions": [],
      "result": {
        "value": 1.1,
        "unit": "1"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.7, таблица 5.4",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "table"
    },
    {
      "step_id": "gamma_c2",
      "expression": "\\gamma_{c2}",
      "substitutions": [],
      "result": {
        "value": 1.0,
        "unit": "1"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.7, таблица 5.4",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "table"
    },
    {
      "step_id": "k",
      "expression": "k",
      "substitutions": [],
      "result": {
        "value": 1.0,
        "unit": "1"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.7, экспликация k",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "table"
    },
    {
      "step_id": "M_gamma",
      "expression": "M_{\\gamma} = M_{\\gamma}\\left(\\varphi_{II}\\right)",
      "substitutions": [
        {
          "value": 20.0,
          "unit": "deg",
          "symbol": "phi_II"
        }
      ],
      "result": {
        "value": 0.51,
        "unit": "1"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.7, таблица 5.5",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "table"
    },
    {
      "step_id": "M_q",
      "expression": "M_{q} = M_{q}\\left(\\varphi_{II}\\right)",
      "substitutions": [
        {
          "value": 20.0,
          "unit": "deg",
          "symbol": "phi_II"
        }
      ],
      "result": {
        "value": 3.06,
        "unit": "1"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.7, таблица 5.5",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "table"
    },
    {
      "step_id": "M_c",
      "expression": "M_{c} = M_{c}\\left(\\varphi_{II}\\right)",
      "substitutions": [
        {
          "value": 20.0,
          "unit": "deg",
          "symbol": "phi_II"
        }
      ],
      "result": {
        "value": 5.66,
        "unit": "1"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.7, таблица 5.5",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "table"
    },
    {
      "step_id": "k_z",
      "expression": "k_{z}=1",
      "substitutions": [],
      "result": {
        "value": 1.0,
        "unit": "1"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.7, экспликация k_z",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "step_id": "R",
      "expression": "R=\\frac{\\gamma_{c1}\\gamma_{c2}}{k}\\left[M_{\\gamma}k_{z}b\\gamma_{II}+M_{q}d_{1}\\gamma'_{II}+(M_{q}-1)d_{b}\\gamma'_{II}+M_{c}c_{II}\\right]",
      "substitutions": [
        {
          "value": 1.1,
          "unit": "1",
          "symbol": "gamma_c1"
        },
        {
          "value": 1.0,
          "unit": "1",
          "symbol": "gamma_c2"
        },
        {
          "value": 1.0,
          "unit": "1",
          "symbol": "k"
        },
        {
          "value": 0.51,
          "unit": "1",
          "symbol": "M_gamma"
        },
        {
          "value": 1.0,
          "unit": "1",
          "symbol": "k_z"
        },
        {
          "value": 2.0,
          "unit": "m",
          "symbol": "b"
        },
        {
          "value": 20.0,
          "unit": "kN/m3",
          "symbol": "gamma_II"
        },
        {
          "value": 3.06,
          "unit": "1",
          "symbol": "M_q"
        },
        {
          "value": 1.0,
          "unit": "m",
          "symbol": "d_1"
        },
        {
          "value": 20.0,
          "unit": "kN/m3",
          "symbol": "gamma_II_prime"
        },
        {
          "value": 0.0,
          "unit": "m",
          "symbol": "d_b"
        },
        {
          "value": 5.66,
          "unit": "1",
          "symbol": "M_c"
        },
        {
          "value": 10.0,
          "unit": "kPa",
          "symbol": "c_II"
        }
      ],
      "result": {
        "value": 152.02,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.7, формула (5.7)",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "kind": "engineer_formula",
      "step_id": "A",
      "expression": "A=b l",
      "substitutions": [
        {
          "value": 2.0,
          "unit": "m",
          "symbol": "b"
        },
        {
          "value": 3.0,
          "unit": "m",
          "symbol": "l"
        }
      ],
      "result": {
        "value": 6.0,
        "unit": "m2"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Геометрия прямоугольной подошвы: A=b*l, Wx=l*b²/6, Wy=b*l²/6; инженерный контракт 2026-11-08."
      }
    },
    {
      "kind": "engineer_formula",
      "step_id": "Wx",
      "expression": "W_x=l b^2/6",
      "substitutions": [
        {
          "value": 2.0,
          "unit": "m",
          "symbol": "b"
        },
        {
          "value": 3.0,
          "unit": "m",
          "symbol": "l"
        }
      ],
      "result": {
        "value": 2.0,
        "unit": "m3"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Геометрия прямоугольной подошвы: A=b*l, Wx=l*b²/6, Wy=b*l²/6; инженерный контракт 2026-11-08."
      }
    },
    {
      "kind": "engineer_formula",
      "step_id": "Wy",
      "expression": "W_y=b l^2/6",
      "substitutions": [
        {
          "value": 2.0,
          "unit": "m",
          "symbol": "b"
        },
        {
          "value": 3.0,
          "unit": "m",
          "symbol": "l"
        }
      ],
      "result": {
        "value": 3.0,
        "unit": "m3"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Геометрия прямоугольной подошвы: A=b*l, Wx=l*b²/6, Wy=b*l²/6; инженерный контракт 2026-11-08."
      }
    },
    {
      "kind": "engineer_formula",
      "step_id": "Mx_base",
      "expression": "M_{x,base}=M_x+Q_x h",
      "substitutions": [
        {
          "value": 240.0,
          "unit": "kN*m",
          "symbol": "Mx"
        },
        {
          "value": 0.0,
          "unit": "kN",
          "symbol": "Qx"
        },
        {
          "value": 1.0,
          "unit": "m",
          "symbol": "h"
        }
      ],
      "result": {
        "value": 240.0,
        "unit": "kN*m"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Подписанный перенос нагрузок к подошве M_base=M+Q*h; оси x=b и y=l; инженерный контракт 2026-11-08."
      }
    },
    {
      "kind": "engineer_formula",
      "step_id": "My_base",
      "expression": "M_{y,base}=M_y+Q_y h",
      "substitutions": [
        {
          "value": 0.0,
          "unit": "kN*m",
          "symbol": "My"
        },
        {
          "value": 0.0,
          "unit": "kN",
          "symbol": "Qy"
        },
        {
          "value": 1.0,
          "unit": "m",
          "symbol": "h"
        }
      ],
      "result": {
        "value": 0.0,
        "unit": "kN*m"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Подписанный перенос нагрузок к подошве M_base=M+Q*h; оси x=b и y=l; инженерный контракт 2026-11-08."
      }
    },
    {
      "step_id": "gamma_mt",
      "expression": "\\gamma_{mt}",
      "substitutions": [],
      "result": {
        "value": 20.0,
        "unit": "kN/m3"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.28, explanation of formula (5.11)",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "table"
    },
    {
      "step_id": "p",
      "expression": "p_{+}=\\frac{N}{A}+\\gamma_{mt}d+\\frac{M}{W}",
      "substitutions": [
        {
          "value": 600.0,
          "unit": "kN",
          "symbol": "N"
        },
        {
          "value": 6.0,
          "unit": "m2",
          "symbol": "A"
        },
        {
          "value": 20.0,
          "unit": "kN/m3",
          "symbol": "gamma_mt"
        },
        {
          "value": 1.0,
          "unit": "m",
          "symbol": "d"
        },
        {
          "value": 0.0,
          "unit": "kN*m",
          "symbol": "M"
        },
        {
          "value": 2.0,
          "unit": "m3",
          "symbol": "W"
        }
      ],
      "result": {
        "value": 120.0,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.28, formula (5.11)",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "kind": "engineer_formula",
      "step_id": "V",
      "expression": "V=N+\\gamma_{mt} d A",
      "substitutions": [
        {
          "value": 600.0,
          "unit": "kN",
          "symbol": "N"
        },
        {
          "value": 20.0,
          "unit": "kN/m3",
          "symbol": "gamma_mt"
        },
        {
          "value": 1.0,
          "unit": "m",
          "symbol": "d"
        },
        {
          "value": 6.0,
          "unit": "m2",
          "symbol": "A"
        }
      ],
      "result": {
        "value": 720.0,
        "unit": "kN"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08."
      }
    },
    {
      "step_id": "p_x_min",
      "expression": "p_{-}=\\frac{N}{A}+\\gamma_{mt}d-\\frac{M}{W}",
      "substitutions": [
        {
          "value": 600.0,
          "unit": "kN",
          "symbol": "N"
        },
        {
          "value": 6.0,
          "unit": "m2",
          "symbol": "A"
        },
        {
          "value": 20.0,
          "unit": "kN/m3",
          "symbol": "gamma_mt"
        },
        {
          "value": 1.0,
          "unit": "m",
          "symbol": "d"
        },
        {
          "value": 240.0,
          "unit": "kN*m",
          "symbol": "M"
        },
        {
          "value": 2.0,
          "unit": "m3",
          "symbol": "W"
        }
      ],
      "result": {
        "value": 0.0,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.28, formula (5.11)",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "step_id": "p_x_max",
      "expression": "p_{+}=\\frac{N}{A}+\\gamma_{mt}d+\\frac{M}{W}",
      "substitutions": [
        {
          "value": 600.0,
          "unit": "kN",
          "symbol": "N"
        },
        {
          "value": 6.0,
          "unit": "m2",
          "symbol": "A"
        },
        {
          "value": 20.0,
          "unit": "kN/m3",
          "symbol": "gamma_mt"
        },
        {
          "value": 1.0,
          "unit": "m",
          "symbol": "d"
        },
        {
          "value": 240.0,
          "unit": "kN*m",
          "symbol": "M"
        },
        {
          "value": 2.0,
          "unit": "m3",
          "symbol": "W"
        }
      ],
      "result": {
        "value": 240.0,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.28, formula (5.11)",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "kind": "engineer_formula",
      "step_id": "e_x",
      "expression": "e_x=|M_{x,base}|/V",
      "substitutions": [
        {
          "value": 240.0,
          "unit": "kN*m",
          "symbol": "Mx_base"
        },
        {
          "value": 720.0,
          "unit": "kN",
          "symbol": "V"
        }
      ],
      "result": {
        "value": 0.3333333333333333,
        "unit": "m"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08."
      }
    },
    {
      "step_id": "relative_eccentricity_x",
      "expression": "e/l\\leq1/6",
      "substitutions": [
        {
          "value": 0.16666666666666666,
          "unit": "1",
          "symbol": "e/L"
        },
        {
          "value": 1.0,
          "unit": "1",
          "symbol": "numerator"
        },
        {
          "value": 6.0,
          "unit": "1",
          "symbol": "denominator"
        }
      ],
      "result": {
        "value": 1.0,
        "unit": "1"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.28, applicability of formula (5.11)",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "step_id": "pressure_diagram_x",
      "expression": "e=l/6",
      "substitutions": [
        {
          "value": 0.3333333333333333,
          "unit": "m",
          "symbol": "e"
        },
        {
          "value": 2.0,
          "unit": "m",
          "symbol": "l"
        }
      ],
      "result": {
        "value": 0.3333333333333333,
        "unit": "m"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.27, figure 5.1",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "step_id": "p_y_min",
      "expression": "p_{-}=\\frac{N}{A}+\\gamma_{mt}d-\\frac{M}{W}",
      "substitutions": [
        {
          "value": 600.0,
          "unit": "kN",
          "symbol": "N"
        },
        {
          "value": 6.0,
          "unit": "m2",
          "symbol": "A"
        },
        {
          "value": 20.0,
          "unit": "kN/m3",
          "symbol": "gamma_mt"
        },
        {
          "value": 1.0,
          "unit": "m",
          "symbol": "d"
        },
        {
          "value": 0.0,
          "unit": "kN*m",
          "symbol": "M"
        },
        {
          "value": 3.0,
          "unit": "m3",
          "symbol": "W"
        }
      ],
      "result": {
        "value": 120.0,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.28, formula (5.11)",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "step_id": "p_y_max",
      "expression": "p_{+}=\\frac{N}{A}+\\gamma_{mt}d+\\frac{M}{W}",
      "substitutions": [
        {
          "value": 600.0,
          "unit": "kN",
          "symbol": "N"
        },
        {
          "value": 6.0,
          "unit": "m2",
          "symbol": "A"
        },
        {
          "value": 20.0,
          "unit": "kN/m3",
          "symbol": "gamma_mt"
        },
        {
          "value": 1.0,
          "unit": "m",
          "symbol": "d"
        },
        {
          "value": 0.0,
          "unit": "kN*m",
          "symbol": "M"
        },
        {
          "value": 3.0,
          "unit": "m3",
          "symbol": "W"
        }
      ],
      "result": {
        "value": 120.0,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.28, formula (5.11)",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "kind": "engineer_formula",
      "step_id": "e_y",
      "expression": "e_y=|M_{y,base}|/V",
      "substitutions": [
        {
          "value": 0.0,
          "unit": "kN*m",
          "symbol": "My_base"
        },
        {
          "value": 720.0,
          "unit": "kN",
          "symbol": "V"
        }
      ],
      "result": {
        "value": 0.0,
        "unit": "m"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08."
      }
    },
    {
      "step_id": "relative_eccentricity_y",
      "expression": "e/l\\leq1/6",
      "substitutions": [
        {
          "value": 0.0,
          "unit": "1",
          "symbol": "e/L"
        },
        {
          "value": 1.0,
          "unit": "1",
          "symbol": "numerator"
        },
        {
          "value": 6.0,
          "unit": "1",
          "symbol": "denominator"
        }
      ],
      "result": {
        "value": 1.0,
        "unit": "1"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.28, applicability of formula (5.11)",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "step_id": "pressure_diagram_y",
      "expression": "e<l/6",
      "substitutions": [
        {
          "value": 0.0,
          "unit": "m",
          "symbol": "e"
        },
        {
          "value": 3.0,
          "unit": "m",
          "symbol": "l"
        }
      ],
      "result": {
        "value": 0.0,
        "unit": "m"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.27, figure 5.1",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "step_id": "corner_component_pp",
      "expression": "P_{\\max}=\\frac{N}{A}+\\gamma_{mt}d+\\frac{M_x}{W_x}+\\frac{M_y}{W_y}",
      "substitutions": [
        {
          "value": 600.0,
          "unit": "kN",
          "symbol": "N"
        },
        {
          "value": 6.0,
          "unit": "m2",
          "symbol": "A"
        },
        {
          "value": 20.0,
          "unit": "kN/m3",
          "symbol": "gamma_mt"
        },
        {
          "value": 1.0,
          "unit": "m",
          "symbol": "d"
        },
        {
          "value": 240.0,
          "unit": "kN*m",
          "symbol": "M_x"
        },
        {
          "value": 2.0,
          "unit": "m3",
          "symbol": "W_x"
        },
        {
          "value": 0.0,
          "unit": "kN*m",
          "symbol": "M_y"
        },
        {
          "value": 3.0,
          "unit": "m3",
          "symbol": "W_y"
        }
      ],
      "result": {
        "value": 240.0,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.29, formula (5.15)",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "kind": "engineer_formula",
      "step_id": "p_corner_pp",
      "expression": "p_{pp}=p+s_x M_{x,base}/W_x+s_y M_{y,base}/W_y",
      "substitutions": [
        {
          "value": 120.0,
          "unit": "kPa",
          "symbol": "p"
        },
        {
          "value": 240.0,
          "unit": "kN*m",
          "symbol": "Mx_base"
        },
        {
          "value": 2.0,
          "unit": "m3",
          "symbol": "Wx"
        },
        {
          "value": 0.0,
          "unit": "kN*m",
          "symbol": "My_base"
        },
        {
          "value": 3.0,
          "unit": "m3",
          "symbol": "Wy"
        },
        {
          "value": 1.0,
          "unit": "1",
          "symbol": "sign_x_pp"
        },
        {
          "value": 1.0,
          "unit": "1",
          "symbol": "sign_y_pp"
        },
        {
          "value": 240.0,
          "unit": "kPa",
          "symbol": "corner_component_pp"
        }
      ],
      "result": {
        "value": 240.0,
        "unit": "kPa"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08."
      }
    },
    {
      "step_id": "corner_component_pm",
      "expression": "P_{\\max}=\\frac{N}{A}+\\gamma_{mt}d+\\frac{M_x}{W_x}+\\frac{M_y}{W_y}",
      "substitutions": [
        {
          "value": 600.0,
          "unit": "kN",
          "symbol": "N"
        },
        {
          "value": 6.0,
          "unit": "m2",
          "symbol": "A"
        },
        {
          "value": 20.0,
          "unit": "kN/m3",
          "symbol": "gamma_mt"
        },
        {
          "value": 1.0,
          "unit": "m",
          "symbol": "d"
        },
        {
          "value": 240.0,
          "unit": "kN*m",
          "symbol": "M_x"
        },
        {
          "value": 2.0,
          "unit": "m3",
          "symbol": "W_x"
        },
        {
          "value": -0.0,
          "unit": "kN*m",
          "symbol": "M_y"
        },
        {
          "value": 3.0,
          "unit": "m3",
          "symbol": "W_y"
        }
      ],
      "result": {
        "value": 240.0,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.29, formula (5.15)",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "kind": "engineer_formula",
      "step_id": "p_corner_pm",
      "expression": "p_{pm}=p+s_x M_{x,base}/W_x+s_y M_{y,base}/W_y",
      "substitutions": [
        {
          "value": 120.0,
          "unit": "kPa",
          "symbol": "p"
        },
        {
          "value": 240.0,
          "unit": "kN*m",
          "symbol": "Mx_base"
        },
        {
          "value": 2.0,
          "unit": "m3",
          "symbol": "Wx"
        },
        {
          "value": 0.0,
          "unit": "kN*m",
          "symbol": "My_base"
        },
        {
          "value": 3.0,
          "unit": "m3",
          "symbol": "Wy"
        },
        {
          "value": 1.0,
          "unit": "1",
          "symbol": "sign_x_pm"
        },
        {
          "value": -1.0,
          "unit": "1",
          "symbol": "sign_y_pm"
        },
        {
          "value": 240.0,
          "unit": "kPa",
          "symbol": "corner_component_pm"
        }
      ],
      "result": {
        "value": 240.0,
        "unit": "kPa"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08."
      }
    },
    {
      "step_id": "corner_component_mp",
      "expression": "P_{\\max}=\\frac{N}{A}+\\gamma_{mt}d+\\frac{M_x}{W_x}+\\frac{M_y}{W_y}",
      "substitutions": [
        {
          "value": 600.0,
          "unit": "kN",
          "symbol": "N"
        },
        {
          "value": 6.0,
          "unit": "m2",
          "symbol": "A"
        },
        {
          "value": 20.0,
          "unit": "kN/m3",
          "symbol": "gamma_mt"
        },
        {
          "value": 1.0,
          "unit": "m",
          "symbol": "d"
        },
        {
          "value": -240.0,
          "unit": "kN*m",
          "symbol": "M_x"
        },
        {
          "value": 2.0,
          "unit": "m3",
          "symbol": "W_x"
        },
        {
          "value": 0.0,
          "unit": "kN*m",
          "symbol": "M_y"
        },
        {
          "value": 3.0,
          "unit": "m3",
          "symbol": "W_y"
        }
      ],
      "result": {
        "value": 0.0,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.29, formula (5.15)",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "kind": "engineer_formula",
      "step_id": "p_corner_mp",
      "expression": "p_{mp}=p+s_x M_{x,base}/W_x+s_y M_{y,base}/W_y",
      "substitutions": [
        {
          "value": 120.0,
          "unit": "kPa",
          "symbol": "p"
        },
        {
          "value": 240.0,
          "unit": "kN*m",
          "symbol": "Mx_base"
        },
        {
          "value": 2.0,
          "unit": "m3",
          "symbol": "Wx"
        },
        {
          "value": 0.0,
          "unit": "kN*m",
          "symbol": "My_base"
        },
        {
          "value": 3.0,
          "unit": "m3",
          "symbol": "Wy"
        },
        {
          "value": -1.0,
          "unit": "1",
          "symbol": "sign_x_mp"
        },
        {
          "value": 1.0,
          "unit": "1",
          "symbol": "sign_y_mp"
        },
        {
          "value": 0.0,
          "unit": "kPa",
          "symbol": "corner_component_mp"
        }
      ],
      "result": {
        "value": 0.0,
        "unit": "kPa"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08."
      }
    },
    {
      "step_id": "corner_component_mm",
      "expression": "P_{\\max}=\\frac{N}{A}+\\gamma_{mt}d+\\frac{M_x}{W_x}+\\frac{M_y}{W_y}",
      "substitutions": [
        {
          "value": 600.0,
          "unit": "kN",
          "symbol": "N"
        },
        {
          "value": 6.0,
          "unit": "m2",
          "symbol": "A"
        },
        {
          "value": 20.0,
          "unit": "kN/m3",
          "symbol": "gamma_mt"
        },
        {
          "value": 1.0,
          "unit": "m",
          "symbol": "d"
        },
        {
          "value": -240.0,
          "unit": "kN*m",
          "symbol": "M_x"
        },
        {
          "value": 2.0,
          "unit": "m3",
          "symbol": "W_x"
        },
        {
          "value": -0.0,
          "unit": "kN*m",
          "symbol": "M_y"
        },
        {
          "value": 3.0,
          "unit": "m3",
          "symbol": "W_y"
        }
      ],
      "result": {
        "value": 0.0,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.29, formula (5.15)",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "kind": "engineer_formula",
      "step_id": "p_corner_mm",
      "expression": "p_{mm}=p+s_x M_{x,base}/W_x+s_y M_{y,base}/W_y",
      "substitutions": [
        {
          "value": 120.0,
          "unit": "kPa",
          "symbol": "p"
        },
        {
          "value": 240.0,
          "unit": "kN*m",
          "symbol": "Mx_base"
        },
        {
          "value": 2.0,
          "unit": "m3",
          "symbol": "Wx"
        },
        {
          "value": 0.0,
          "unit": "kN*m",
          "symbol": "My_base"
        },
        {
          "value": 3.0,
          "unit": "m3",
          "symbol": "Wy"
        },
        {
          "value": -1.0,
          "unit": "1",
          "symbol": "sign_x_mm"
        },
        {
          "value": -1.0,
          "unit": "1",
          "symbol": "sign_y_mm"
        },
        {
          "value": 0.0,
          "unit": "kPa",
          "symbol": "corner_component_mm"
        }
      ],
      "result": {
        "value": 0.0,
        "unit": "kPa"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08."
      }
    },
    {
      "kind": "engineer_formula",
      "step_id": "p_corner_min",
      "expression": "p_{corner,min}=\\min(p_{++},p_{+-},p_{-+},p_{--})",
      "substitutions": [
        {
          "value": 240.0,
          "unit": "kPa",
          "symbol": "p_corner_pp"
        },
        {
          "value": 240.0,
          "unit": "kPa",
          "symbol": "p_corner_pm"
        },
        {
          "value": 0.0,
          "unit": "kPa",
          "symbol": "p_corner_mp"
        },
        {
          "value": 0.0,
          "unit": "kPa",
          "symbol": "p_corner_mm"
        }
      ],
      "result": {
        "value": 0.0,
        "unit": "kPa"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Полный контакт прямоугольной подошвы: минимум четырёх подписанных угловых давлений неотрицателен; решение инженера 2026-11-08."
      }
    },
    {
      "kind": "engineer_formula",
      "step_id": "p_corner_max",
      "expression": "p_{corner,max}=\\max(p_{++},p_{+-},p_{-+},p_{--})",
      "substitutions": [
        {
          "value": 240.0,
          "unit": "kPa",
          "symbol": "p_corner_pp"
        },
        {
          "value": 240.0,
          "unit": "kPa",
          "symbol": "p_corner_pm"
        },
        {
          "value": 0.0,
          "unit": "kPa",
          "symbol": "p_corner_mp"
        },
        {
          "value": 0.0,
          "unit": "kPa",
          "symbol": "p_corner_mm"
        }
      ],
      "result": {
        "value": 240.0,
        "unit": "kPa"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08."
      }
    },
    {
      "step_id": "edge_limit_multiplier",
      "expression": "edge_limit_multiplier",
      "substitutions": [],
      "result": {
        "value": 1.2,
        "unit": "1"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.26",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "table"
    },
    {
      "step_id": "edge_limit",
      "expression": "p_{edge,lim}=\\lambda_e R",
      "substitutions": [
        {
          "value": 1.2,
          "unit": "1",
          "symbol": "edge_limit_multiplier"
        },
        {
          "value": 152.02,
          "unit": "kPa",
          "symbol": "R"
        }
      ],
      "result": {
        "value": 182.424,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.26",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "step_id": "corner_limit_multiplier",
      "expression": "corner_limit_multiplier",
      "substitutions": [],
      "result": {
        "value": 1.5,
        "unit": "1"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.26",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "table"
    },
    {
      "step_id": "corner_limit",
      "expression": "p_{corner,lim}=\\lambda_c R",
      "substitutions": [
        {
          "value": 1.5,
          "unit": "1",
          "symbol": "corner_limit_multiplier"
        },
        {
          "value": 152.02,
          "unit": "kPa",
          "symbol": "R"
        }
      ],
      "result": {
        "value": 228.03000000000003,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.26",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "step_id": "p_le_R",
      "expression": "p \\le R",
      "substitutions": [
        {
          "value": 120.0,
          "unit": "kPa",
          "symbol": "p"
        },
        {
          "value": 152.02,
          "unit": "kPa",
          "symbol": "R"
        }
      ],
      "result": {
        "value": 120.0,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.7",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "check",
      "operator": "le",
      "right": {
        "value": 152.02,
        "unit": "kPa"
      },
      "passed": true
    },
    {
      "step_id": "p_x_max_le_limit",
      "expression": "p_x_max \\le edge_limit",
      "substitutions": [
        {
          "value": 240.0,
          "unit": "kPa",
          "symbol": "p_x_max"
        },
        {
          "value": 182.424,
          "unit": "kPa",
          "symbol": "edge_limit"
        }
      ],
      "result": {
        "value": 240.0,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.26",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "check",
      "operator": "le",
      "right": {
        "value": 182.424,
        "unit": "kPa"
      },
      "passed": false
    },
    {
      "step_id": "p_y_max_le_limit",
      "expression": "p_y_max \\le edge_limit",
      "substitutions": [
        {
          "value": 120.0,
          "unit": "kPa",
          "symbol": "p_y_max"
        },
        {
          "value": 182.424,
          "unit": "kPa",
          "symbol": "edge_limit"
        }
      ],
      "result": {
        "value": 120.0,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.26",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "check",
      "operator": "le",
      "right": {
        "value": 182.424,
        "unit": "kPa"
      },
      "passed": true
    },
    {
      "step_id": "p_corner_max_le_limit",
      "expression": "p_corner_max \\le corner_limit",
      "substitutions": [
        {
          "value": 240.0,
          "unit": "kPa",
          "symbol": "p_corner_max"
        },
        {
          "value": 228.03000000000003,
          "unit": "kPa",
          "symbol": "corner_limit"
        }
      ],
      "result": {
        "value": 240.0,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "СП 22.13330.2016",
          "edition": "2016 (с Изменениями N 1, 2, 3, 4, 5)",
          "clause": "5.6.26",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "check",
      "operator": "le",
      "right": {
        "value": 228.03000000000003,
        "unit": "kPa"
      },
      "passed": false
    }
  ],
  "unverified_step_count": 30,
  "result_id": "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb",
  "parameter_source": {
    "kind": "interim",
    "data_sha256": "faaa0724af57ca6c8066f558c4e75c2785d099b34cbfb07c4a85892fdc3b68fe", // pragma: allowlist secret
    "profile": "strict"
  }
} satisfies ResultEnvelope

export const loadsZeroContactJson = "{\"engine_version\":\"0.1.0\",\"input_hash\":\"082595b7d7fd71d3242a407044bae8c0fc4e191b35f080bb5f1b9ddd59c89dc4\",\"outputs\":[{\"value\":152.02,\"unit\":\"kPa\",\"quantity\":\"R\",\"rounding_rule\":{\"decimals\":2,\"mode\":\"half_up\"},\"rounding_source\":{\"engineer\":\"Аким\",\"rationale\":\"Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются.\"}},{\"value\":120.0,\"unit\":\"kPa\",\"quantity\":\"p\",\"rounding_rule\":{\"decimals\":2,\"mode\":\"half_up\"},\"rounding_source\":{\"engineer\":\"Аким\",\"rationale\":\"Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются.\"}},{\"value\":0.0,\"unit\":\"kPa\",\"quantity\":\"p_x_min\",\"rounding_rule\":{\"decimals\":2,\"mode\":\"half_up\"},\"rounding_source\":{\"engineer\":\"Аким\",\"rationale\":\"Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются.\"}},{\"value\":240.0,\"unit\":\"kPa\",\"quantity\":\"p_x_max\",\"rounding_rule\":{\"decimals\":2,\"mode\":\"half_up\"},\"rounding_source\":{\"engineer\":\"Аким\",\"rationale\":\"Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются.\"}},{\"value\":120.0,\"unit\":\"kPa\",\"quantity\":\"p_y_min\",\"rounding_rule\":{\"decimals\":2,\"mode\":\"half_up\"},\"rounding_source\":{\"engineer\":\"Аким\",\"rationale\":\"Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются.\"}},{\"value\":120.0,\"unit\":\"kPa\",\"quantity\":\"p_y_max\",\"rounding_rule\":{\"decimals\":2,\"mode\":\"half_up\"},\"rounding_source\":{\"engineer\":\"Аким\",\"rationale\":\"Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются.\"}},{\"value\":240.0,\"unit\":\"kPa\",\"quantity\":\"p_corner_pp\",\"rounding_rule\":{\"decimals\":2,\"mode\":\"half_up\"},\"rounding_source\":{\"engineer\":\"Аким\",\"rationale\":\"Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются.\"}},{\"value\":240.0,\"unit\":\"kPa\",\"quantity\":\"p_corner_pm\",\"rounding_rule\":{\"decimals\":2,\"mode\":\"half_up\"},\"rounding_source\":{\"engineer\":\"Аким\",\"rationale\":\"Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются.\"}},{\"value\":0.0,\"unit\":\"kPa\",\"quantity\":\"p_corner_mp\",\"rounding_rule\":{\"decimals\":2,\"mode\":\"half_up\"},\"rounding_source\":{\"engineer\":\"Аким\",\"rationale\":\"Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются.\"}},{\"value\":0.0,\"unit\":\"kPa\",\"quantity\":\"p_corner_mm\",\"rounding_rule\":{\"decimals\":2,\"mode\":\"half_up\"},\"rounding_source\":{\"engineer\":\"Аким\",\"rationale\":\"Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются.\"}}],\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7, таблица 5.4\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"},{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7, экспликация k\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"},{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7, таблица 5.5\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"},{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7, экспликация k_z\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"},{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7, формула (5.7)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"},{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.28, explanation of formula (5.11)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"},{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.28, formula (5.11)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"},{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.28, applicability of formula (5.11)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"},{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.27, figure 5.1\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"},{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.29, formula (5.15)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"},{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.26\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"},{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"engineer_rules\":[{\"engineer\":\"Аким\",\"rationale\":\"Геометрия прямоугольной подошвы: A=b*l, Wx=l*b²/6, Wy=b*l²/6; инженерный контракт 2026-11-08.\"},{\"engineer\":\"Аким\",\"rationale\":\"Подписанный перенос нагрузок к подошве M_base=M+Q*h; оси x=b и y=l; инженерный контракт 2026-11-08.\"},{\"engineer\":\"Аким\",\"rationale\":\"Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08.\"},{\"engineer\":\"Аким\",\"rationale\":\"Полный контакт прямоугольной подошвы: минимум четырёх подписанных угловых давлений неотрицателен; решение инженера 2026-11-08.\"},{\"engineer\":\"Аким\",\"rationale\":\"Округление выходов до 0.01 кПа, half_up; решение инженера 2026-11-08. Промежуточные значения и сравнения не округляются.\"}],\"verdict\":\"fail\",\"verdict_reason\":{\"kind\":\"check\",\"step_id\":\"p_x_max_le_limit\"},\"warnings\":[],\"trace\":[{\"step_id\":\"gamma_c1\",\"expression\":\"\\\\gamma_{c1}\",\"substitutions\":[],\"result\":{\"value\":1.1,\"unit\":\"1\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7, таблица 5.4\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"table\"},{\"step_id\":\"gamma_c2\",\"expression\":\"\\\\gamma_{c2}\",\"substitutions\":[],\"result\":{\"value\":1.0,\"unit\":\"1\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7, таблица 5.4\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"table\"},{\"step_id\":\"k\",\"expression\":\"k\",\"substitutions\":[],\"result\":{\"value\":1.0,\"unit\":\"1\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7, экспликация k\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"table\"},{\"step_id\":\"M_gamma\",\"expression\":\"M_{\\\\gamma} = M_{\\\\gamma}\\\\left(\\\\varphi_{II}\\\\right)\",\"substitutions\":[{\"value\":20.0,\"unit\":\"deg\",\"symbol\":\"phi_II\"}],\"result\":{\"value\":0.51,\"unit\":\"1\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7, таблица 5.5\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"table\"},{\"step_id\":\"M_q\",\"expression\":\"M_{q} = M_{q}\\\\left(\\\\varphi_{II}\\\\right)\",\"substitutions\":[{\"value\":20.0,\"unit\":\"deg\",\"symbol\":\"phi_II\"}],\"result\":{\"value\":3.06,\"unit\":\"1\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7, таблица 5.5\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"table\"},{\"step_id\":\"M_c\",\"expression\":\"M_{c} = M_{c}\\\\left(\\\\varphi_{II}\\\\right)\",\"substitutions\":[{\"value\":20.0,\"unit\":\"deg\",\"symbol\":\"phi_II\"}],\"result\":{\"value\":5.66,\"unit\":\"1\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7, таблица 5.5\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"table\"},{\"step_id\":\"k_z\",\"expression\":\"k_{z}=1\",\"substitutions\":[],\"result\":{\"value\":1.0,\"unit\":\"1\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7, экспликация k_z\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"step_id\":\"R\",\"expression\":\"R=\\\\frac{\\\\gamma_{c1}\\\\gamma_{c2}}{k}\\\\left[M_{\\\\gamma}k_{z}b\\\\gamma_{II}+M_{q}d_{1}\\\\gamma'_{II}+(M_{q}-1)d_{b}\\\\gamma'_{II}+M_{c}c_{II}\\\\right]\",\"substitutions\":[{\"value\":1.1,\"unit\":\"1\",\"symbol\":\"gamma_c1\"},{\"value\":1.0,\"unit\":\"1\",\"symbol\":\"gamma_c2\"},{\"value\":1.0,\"unit\":\"1\",\"symbol\":\"k\"},{\"value\":0.51,\"unit\":\"1\",\"symbol\":\"M_gamma\"},{\"value\":1.0,\"unit\":\"1\",\"symbol\":\"k_z\"},{\"value\":2.0,\"unit\":\"m\",\"symbol\":\"b\"},{\"value\":20.0,\"unit\":\"kN/m3\",\"symbol\":\"gamma_II\"},{\"value\":3.06,\"unit\":\"1\",\"symbol\":\"M_q\"},{\"value\":1.0,\"unit\":\"m\",\"symbol\":\"d_1\"},{\"value\":20.0,\"unit\":\"kN/m3\",\"symbol\":\"gamma_II_prime\"},{\"value\":0.0,\"unit\":\"m\",\"symbol\":\"d_b\"},{\"value\":5.66,\"unit\":\"1\",\"symbol\":\"M_c\"},{\"value\":10.0,\"unit\":\"kPa\",\"symbol\":\"c_II\"}],\"result\":{\"value\":152.02,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7, формула (5.7)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"kind\":\"engineer_formula\",\"step_id\":\"A\",\"expression\":\"A=b l\",\"substitutions\":[{\"value\":2.0,\"unit\":\"m\",\"symbol\":\"b\"},{\"value\":3.0,\"unit\":\"m\",\"symbol\":\"l\"}],\"result\":{\"value\":6.0,\"unit\":\"m2\"},\"source\":{\"engineer\":\"Аким\",\"rationale\":\"Геометрия прямоугольной подошвы: A=b*l, Wx=l*b²/6, Wy=b*l²/6; инженерный контракт 2026-11-08.\"}},{\"kind\":\"engineer_formula\",\"step_id\":\"Wx\",\"expression\":\"W_x=l b^2/6\",\"substitutions\":[{\"value\":2.0,\"unit\":\"m\",\"symbol\":\"b\"},{\"value\":3.0,\"unit\":\"m\",\"symbol\":\"l\"}],\"result\":{\"value\":2.0,\"unit\":\"m3\"},\"source\":{\"engineer\":\"Аким\",\"rationale\":\"Геометрия прямоугольной подошвы: A=b*l, Wx=l*b²/6, Wy=b*l²/6; инженерный контракт 2026-11-08.\"}},{\"kind\":\"engineer_formula\",\"step_id\":\"Wy\",\"expression\":\"W_y=b l^2/6\",\"substitutions\":[{\"value\":2.0,\"unit\":\"m\",\"symbol\":\"b\"},{\"value\":3.0,\"unit\":\"m\",\"symbol\":\"l\"}],\"result\":{\"value\":3.0,\"unit\":\"m3\"},\"source\":{\"engineer\":\"Аким\",\"rationale\":\"Геометрия прямоугольной подошвы: A=b*l, Wx=l*b²/6, Wy=b*l²/6; инженерный контракт 2026-11-08.\"}},{\"kind\":\"engineer_formula\",\"step_id\":\"Mx_base\",\"expression\":\"M_{x,base}=M_x+Q_x h\",\"substitutions\":[{\"value\":240.0,\"unit\":\"kN*m\",\"symbol\":\"Mx\"},{\"value\":0.0,\"unit\":\"kN\",\"symbol\":\"Qx\"},{\"value\":1.0,\"unit\":\"m\",\"symbol\":\"h\"}],\"result\":{\"value\":240.0,\"unit\":\"kN*m\"},\"source\":{\"engineer\":\"Аким\",\"rationale\":\"Подписанный перенос нагрузок к подошве M_base=M+Q*h; оси x=b и y=l; инженерный контракт 2026-11-08.\"}},{\"kind\":\"engineer_formula\",\"step_id\":\"My_base\",\"expression\":\"M_{y,base}=M_y+Q_y h\",\"substitutions\":[{\"value\":0.0,\"unit\":\"kN*m\",\"symbol\":\"My\"},{\"value\":0.0,\"unit\":\"kN\",\"symbol\":\"Qy\"},{\"value\":1.0,\"unit\":\"m\",\"symbol\":\"h\"}],\"result\":{\"value\":0.0,\"unit\":\"kN*m\"},\"source\":{\"engineer\":\"Аким\",\"rationale\":\"Подписанный перенос нагрузок к подошве M_base=M+Q*h; оси x=b и y=l; инженерный контракт 2026-11-08.\"}},{\"step_id\":\"gamma_mt\",\"expression\":\"\\\\gamma_{mt}\",\"substitutions\":[],\"result\":{\"value\":20.0,\"unit\":\"kN/m3\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.28, explanation of formula (5.11)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"table\"},{\"step_id\":\"p\",\"expression\":\"p_{+}=\\\\frac{N}{A}+\\\\gamma_{mt}d+\\\\frac{M}{W}\",\"substitutions\":[{\"value\":600.0,\"unit\":\"kN\",\"symbol\":\"N\"},{\"value\":6.0,\"unit\":\"m2\",\"symbol\":\"A\"},{\"value\":20.0,\"unit\":\"kN/m3\",\"symbol\":\"gamma_mt\"},{\"value\":1.0,\"unit\":\"m\",\"symbol\":\"d\"},{\"value\":0.0,\"unit\":\"kN*m\",\"symbol\":\"M\"},{\"value\":2.0,\"unit\":\"m3\",\"symbol\":\"W\"}],\"result\":{\"value\":120.0,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.28, formula (5.11)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"kind\":\"engineer_formula\",\"step_id\":\"V\",\"expression\":\"V=N+\\\\gamma_{mt} d A\",\"substitutions\":[{\"value\":600.0,\"unit\":\"kN\",\"symbol\":\"N\"},{\"value\":20.0,\"unit\":\"kN/m3\",\"symbol\":\"gamma_mt\"},{\"value\":1.0,\"unit\":\"m\",\"symbol\":\"d\"},{\"value\":6.0,\"unit\":\"m2\",\"symbol\":\"A\"}],\"result\":{\"value\":720.0,\"unit\":\"kN\"},\"source\":{\"engineer\":\"Аким\",\"rationale\":\"Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08.\"}},{\"step_id\":\"p_x_min\",\"expression\":\"p_{-}=\\\\frac{N}{A}+\\\\gamma_{mt}d-\\\\frac{M}{W}\",\"substitutions\":[{\"value\":600.0,\"unit\":\"kN\",\"symbol\":\"N\"},{\"value\":6.0,\"unit\":\"m2\",\"symbol\":\"A\"},{\"value\":20.0,\"unit\":\"kN/m3\",\"symbol\":\"gamma_mt\"},{\"value\":1.0,\"unit\":\"m\",\"symbol\":\"d\"},{\"value\":240.0,\"unit\":\"kN*m\",\"symbol\":\"M\"},{\"value\":2.0,\"unit\":\"m3\",\"symbol\":\"W\"}],\"result\":{\"value\":0.0,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.28, formula (5.11)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"step_id\":\"p_x_max\",\"expression\":\"p_{+}=\\\\frac{N}{A}+\\\\gamma_{mt}d+\\\\frac{M}{W}\",\"substitutions\":[{\"value\":600.0,\"unit\":\"kN\",\"symbol\":\"N\"},{\"value\":6.0,\"unit\":\"m2\",\"symbol\":\"A\"},{\"value\":20.0,\"unit\":\"kN/m3\",\"symbol\":\"gamma_mt\"},{\"value\":1.0,\"unit\":\"m\",\"symbol\":\"d\"},{\"value\":240.0,\"unit\":\"kN*m\",\"symbol\":\"M\"},{\"value\":2.0,\"unit\":\"m3\",\"symbol\":\"W\"}],\"result\":{\"value\":240.0,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.28, formula (5.11)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"kind\":\"engineer_formula\",\"step_id\":\"e_x\",\"expression\":\"e_x=|M_{x,base}|/V\",\"substitutions\":[{\"value\":240.0,\"unit\":\"kN*m\",\"symbol\":\"Mx_base\"},{\"value\":720.0,\"unit\":\"kN\",\"symbol\":\"V\"}],\"result\":{\"value\":0.3333333333333333,\"unit\":\"m\"},\"source\":{\"engineer\":\"Аким\",\"rationale\":\"Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08.\"}},{\"step_id\":\"relative_eccentricity_x\",\"expression\":\"e/l\\\\leq1/6\",\"substitutions\":[{\"value\":0.16666666666666666,\"unit\":\"1\",\"symbol\":\"e/L\"},{\"value\":1.0,\"unit\":\"1\",\"symbol\":\"numerator\"},{\"value\":6.0,\"unit\":\"1\",\"symbol\":\"denominator\"}],\"result\":{\"value\":1.0,\"unit\":\"1\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.28, applicability of formula (5.11)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"step_id\":\"pressure_diagram_x\",\"expression\":\"e=l/6\",\"substitutions\":[{\"value\":0.3333333333333333,\"unit\":\"m\",\"symbol\":\"e\"},{\"value\":2.0,\"unit\":\"m\",\"symbol\":\"l\"}],\"result\":{\"value\":0.3333333333333333,\"unit\":\"m\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.27, figure 5.1\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"step_id\":\"p_y_min\",\"expression\":\"p_{-}=\\\\frac{N}{A}+\\\\gamma_{mt}d-\\\\frac{M}{W}\",\"substitutions\":[{\"value\":600.0,\"unit\":\"kN\",\"symbol\":\"N\"},{\"value\":6.0,\"unit\":\"m2\",\"symbol\":\"A\"},{\"value\":20.0,\"unit\":\"kN/m3\",\"symbol\":\"gamma_mt\"},{\"value\":1.0,\"unit\":\"m\",\"symbol\":\"d\"},{\"value\":0.0,\"unit\":\"kN*m\",\"symbol\":\"M\"},{\"value\":3.0,\"unit\":\"m3\",\"symbol\":\"W\"}],\"result\":{\"value\":120.0,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.28, formula (5.11)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"step_id\":\"p_y_max\",\"expression\":\"p_{+}=\\\\frac{N}{A}+\\\\gamma_{mt}d+\\\\frac{M}{W}\",\"substitutions\":[{\"value\":600.0,\"unit\":\"kN\",\"symbol\":\"N\"},{\"value\":6.0,\"unit\":\"m2\",\"symbol\":\"A\"},{\"value\":20.0,\"unit\":\"kN/m3\",\"symbol\":\"gamma_mt\"},{\"value\":1.0,\"unit\":\"m\",\"symbol\":\"d\"},{\"value\":0.0,\"unit\":\"kN*m\",\"symbol\":\"M\"},{\"value\":3.0,\"unit\":\"m3\",\"symbol\":\"W\"}],\"result\":{\"value\":120.0,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.28, formula (5.11)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"kind\":\"engineer_formula\",\"step_id\":\"e_y\",\"expression\":\"e_y=|M_{y,base}|/V\",\"substitutions\":[{\"value\":0.0,\"unit\":\"kN*m\",\"symbol\":\"My_base\"},{\"value\":720.0,\"unit\":\"kN\",\"symbol\":\"V\"}],\"result\":{\"value\":0.0,\"unit\":\"m\"},\"source\":{\"engineer\":\"Аким\",\"rationale\":\"Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08.\"}},{\"step_id\":\"relative_eccentricity_y\",\"expression\":\"e/l\\\\leq1/6\",\"substitutions\":[{\"value\":0.0,\"unit\":\"1\",\"symbol\":\"e/L\"},{\"value\":1.0,\"unit\":\"1\",\"symbol\":\"numerator\"},{\"value\":6.0,\"unit\":\"1\",\"symbol\":\"denominator\"}],\"result\":{\"value\":1.0,\"unit\":\"1\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.28, applicability of formula (5.11)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"step_id\":\"pressure_diagram_y\",\"expression\":\"e<l/6\",\"substitutions\":[{\"value\":0.0,\"unit\":\"m\",\"symbol\":\"e\"},{\"value\":3.0,\"unit\":\"m\",\"symbol\":\"l\"}],\"result\":{\"value\":0.0,\"unit\":\"m\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.27, figure 5.1\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"step_id\":\"corner_component_pp\",\"expression\":\"P_{\\\\max}=\\\\frac{N}{A}+\\\\gamma_{mt}d+\\\\frac{M_x}{W_x}+\\\\frac{M_y}{W_y}\",\"substitutions\":[{\"value\":600.0,\"unit\":\"kN\",\"symbol\":\"N\"},{\"value\":6.0,\"unit\":\"m2\",\"symbol\":\"A\"},{\"value\":20.0,\"unit\":\"kN/m3\",\"symbol\":\"gamma_mt\"},{\"value\":1.0,\"unit\":\"m\",\"symbol\":\"d\"},{\"value\":240.0,\"unit\":\"kN*m\",\"symbol\":\"M_x\"},{\"value\":2.0,\"unit\":\"m3\",\"symbol\":\"W_x\"},{\"value\":0.0,\"unit\":\"kN*m\",\"symbol\":\"M_y\"},{\"value\":3.0,\"unit\":\"m3\",\"symbol\":\"W_y\"}],\"result\":{\"value\":240.0,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.29, formula (5.15)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"kind\":\"engineer_formula\",\"step_id\":\"p_corner_pp\",\"expression\":\"p_{pp}=p+s_x M_{x,base}/W_x+s_y M_{y,base}/W_y\",\"substitutions\":[{\"value\":120.0,\"unit\":\"kPa\",\"symbol\":\"p\"},{\"value\":240.0,\"unit\":\"kN*m\",\"symbol\":\"Mx_base\"},{\"value\":2.0,\"unit\":\"m3\",\"symbol\":\"Wx\"},{\"value\":0.0,\"unit\":\"kN*m\",\"symbol\":\"My_base\"},{\"value\":3.0,\"unit\":\"m3\",\"symbol\":\"Wy\"},{\"value\":1.0,\"unit\":\"1\",\"symbol\":\"sign_x_pp\"},{\"value\":1.0,\"unit\":\"1\",\"symbol\":\"sign_y_pp\"},{\"value\":240.0,\"unit\":\"kPa\",\"symbol\":\"corner_component_pp\"}],\"result\":{\"value\":240.0,\"unit\":\"kPa\"},\"source\":{\"engineer\":\"Аким\",\"rationale\":\"Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08.\"}},{\"step_id\":\"corner_component_pm\",\"expression\":\"P_{\\\\max}=\\\\frac{N}{A}+\\\\gamma_{mt}d+\\\\frac{M_x}{W_x}+\\\\frac{M_y}{W_y}\",\"substitutions\":[{\"value\":600.0,\"unit\":\"kN\",\"symbol\":\"N\"},{\"value\":6.0,\"unit\":\"m2\",\"symbol\":\"A\"},{\"value\":20.0,\"unit\":\"kN/m3\",\"symbol\":\"gamma_mt\"},{\"value\":1.0,\"unit\":\"m\",\"symbol\":\"d\"},{\"value\":240.0,\"unit\":\"kN*m\",\"symbol\":\"M_x\"},{\"value\":2.0,\"unit\":\"m3\",\"symbol\":\"W_x\"},{\"value\":-0.0,\"unit\":\"kN*m\",\"symbol\":\"M_y\"},{\"value\":3.0,\"unit\":\"m3\",\"symbol\":\"W_y\"}],\"result\":{\"value\":240.0,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.29, formula (5.15)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"kind\":\"engineer_formula\",\"step_id\":\"p_corner_pm\",\"expression\":\"p_{pm}=p+s_x M_{x,base}/W_x+s_y M_{y,base}/W_y\",\"substitutions\":[{\"value\":120.0,\"unit\":\"kPa\",\"symbol\":\"p\"},{\"value\":240.0,\"unit\":\"kN*m\",\"symbol\":\"Mx_base\"},{\"value\":2.0,\"unit\":\"m3\",\"symbol\":\"Wx\"},{\"value\":0.0,\"unit\":\"kN*m\",\"symbol\":\"My_base\"},{\"value\":3.0,\"unit\":\"m3\",\"symbol\":\"Wy\"},{\"value\":1.0,\"unit\":\"1\",\"symbol\":\"sign_x_pm\"},{\"value\":-1.0,\"unit\":\"1\",\"symbol\":\"sign_y_pm\"},{\"value\":240.0,\"unit\":\"kPa\",\"symbol\":\"corner_component_pm\"}],\"result\":{\"value\":240.0,\"unit\":\"kPa\"},\"source\":{\"engineer\":\"Аким\",\"rationale\":\"Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08.\"}},{\"step_id\":\"corner_component_mp\",\"expression\":\"P_{\\\\max}=\\\\frac{N}{A}+\\\\gamma_{mt}d+\\\\frac{M_x}{W_x}+\\\\frac{M_y}{W_y}\",\"substitutions\":[{\"value\":600.0,\"unit\":\"kN\",\"symbol\":\"N\"},{\"value\":6.0,\"unit\":\"m2\",\"symbol\":\"A\"},{\"value\":20.0,\"unit\":\"kN/m3\",\"symbol\":\"gamma_mt\"},{\"value\":1.0,\"unit\":\"m\",\"symbol\":\"d\"},{\"value\":-240.0,\"unit\":\"kN*m\",\"symbol\":\"M_x\"},{\"value\":2.0,\"unit\":\"m3\",\"symbol\":\"W_x\"},{\"value\":0.0,\"unit\":\"kN*m\",\"symbol\":\"M_y\"},{\"value\":3.0,\"unit\":\"m3\",\"symbol\":\"W_y\"}],\"result\":{\"value\":0.0,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.29, formula (5.15)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"kind\":\"engineer_formula\",\"step_id\":\"p_corner_mp\",\"expression\":\"p_{mp}=p+s_x M_{x,base}/W_x+s_y M_{y,base}/W_y\",\"substitutions\":[{\"value\":120.0,\"unit\":\"kPa\",\"symbol\":\"p\"},{\"value\":240.0,\"unit\":\"kN*m\",\"symbol\":\"Mx_base\"},{\"value\":2.0,\"unit\":\"m3\",\"symbol\":\"Wx\"},{\"value\":0.0,\"unit\":\"kN*m\",\"symbol\":\"My_base\"},{\"value\":3.0,\"unit\":\"m3\",\"symbol\":\"Wy\"},{\"value\":-1.0,\"unit\":\"1\",\"symbol\":\"sign_x_mp\"},{\"value\":1.0,\"unit\":\"1\",\"symbol\":\"sign_y_mp\"},{\"value\":0.0,\"unit\":\"kPa\",\"symbol\":\"corner_component_mp\"}],\"result\":{\"value\":0.0,\"unit\":\"kPa\"},\"source\":{\"engineer\":\"Аким\",\"rationale\":\"Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08.\"}},{\"step_id\":\"corner_component_mm\",\"expression\":\"P_{\\\\max}=\\\\frac{N}{A}+\\\\gamma_{mt}d+\\\\frac{M_x}{W_x}+\\\\frac{M_y}{W_y}\",\"substitutions\":[{\"value\":600.0,\"unit\":\"kN\",\"symbol\":\"N\"},{\"value\":6.0,\"unit\":\"m2\",\"symbol\":\"A\"},{\"value\":20.0,\"unit\":\"kN/m3\",\"symbol\":\"gamma_mt\"},{\"value\":1.0,\"unit\":\"m\",\"symbol\":\"d\"},{\"value\":-240.0,\"unit\":\"kN*m\",\"symbol\":\"M_x\"},{\"value\":2.0,\"unit\":\"m3\",\"symbol\":\"W_x\"},{\"value\":-0.0,\"unit\":\"kN*m\",\"symbol\":\"M_y\"},{\"value\":3.0,\"unit\":\"m3\",\"symbol\":\"W_y\"}],\"result\":{\"value\":0.0,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.29, formula (5.15)\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"kind\":\"engineer_formula\",\"step_id\":\"p_corner_mm\",\"expression\":\"p_{mm}=p+s_x M_{x,base}/W_x+s_y M_{y,base}/W_y\",\"substitutions\":[{\"value\":120.0,\"unit\":\"kPa\",\"symbol\":\"p\"},{\"value\":240.0,\"unit\":\"kN*m\",\"symbol\":\"Mx_base\"},{\"value\":2.0,\"unit\":\"m3\",\"symbol\":\"Wx\"},{\"value\":0.0,\"unit\":\"kN*m\",\"symbol\":\"My_base\"},{\"value\":3.0,\"unit\":\"m3\",\"symbol\":\"Wy\"},{\"value\":-1.0,\"unit\":\"1\",\"symbol\":\"sign_x_mm\"},{\"value\":-1.0,\"unit\":\"1\",\"symbol\":\"sign_y_mm\"},{\"value\":0.0,\"unit\":\"kPa\",\"symbol\":\"corner_component_mm\"}],\"result\":{\"value\":0.0,\"unit\":\"kPa\"},\"source\":{\"engineer\":\"Аким\",\"rationale\":\"Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08.\"}},{\"kind\":\"engineer_formula\",\"step_id\":\"p_corner_min\",\"expression\":\"p_{corner,min}=\\\\min(p_{++},p_{+-},p_{-+},p_{--})\",\"substitutions\":[{\"value\":240.0,\"unit\":\"kPa\",\"symbol\":\"p_corner_pp\"},{\"value\":240.0,\"unit\":\"kPa\",\"symbol\":\"p_corner_pm\"},{\"value\":0.0,\"unit\":\"kPa\",\"symbol\":\"p_corner_mp\"},{\"value\":0.0,\"unit\":\"kPa\",\"symbol\":\"p_corner_mm\"}],\"result\":{\"value\":0.0,\"unit\":\"kPa\"},\"source\":{\"engineer\":\"Аким\",\"rationale\":\"Полный контакт прямоугольной подошвы: минимум четырёх подписанных угловых давлений неотрицателен; решение инженера 2026-11-08.\"}},{\"kind\":\"engineer_formula\",\"step_id\":\"p_corner_max\",\"expression\":\"p_{corner,max}=\\\\max(p_{++},p_{+-},p_{-+},p_{--})\",\"substitutions\":[{\"value\":240.0,\"unit\":\"kPa\",\"symbol\":\"p_corner_pp\"},{\"value\":240.0,\"unit\":\"kPa\",\"symbol\":\"p_corner_pm\"},{\"value\":0.0,\"unit\":\"kPa\",\"symbol\":\"p_corner_mp\"},{\"value\":0.0,\"unit\":\"kPa\",\"symbol\":\"p_corner_mm\"}],\"result\":{\"value\":240.0,\"unit\":\"kPa\"},\"source\":{\"engineer\":\"Аким\",\"rationale\":\"Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08.\"}},{\"step_id\":\"edge_limit_multiplier\",\"expression\":\"edge_limit_multiplier\",\"substitutions\":[],\"result\":{\"value\":1.2,\"unit\":\"1\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.26\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"table\"},{\"step_id\":\"edge_limit\",\"expression\":\"p_{edge,lim}=\\\\lambda_e R\",\"substitutions\":[{\"value\":1.2,\"unit\":\"1\",\"symbol\":\"edge_limit_multiplier\"},{\"value\":152.02,\"unit\":\"kPa\",\"symbol\":\"R\"}],\"result\":{\"value\":182.424,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.26\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"step_id\":\"corner_limit_multiplier\",\"expression\":\"corner_limit_multiplier\",\"substitutions\":[],\"result\":{\"value\":1.5,\"unit\":\"1\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.26\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"table\"},{\"step_id\":\"corner_limit\",\"expression\":\"p_{corner,lim}=\\\\lambda_c R\",\"substitutions\":[{\"value\":1.5,\"unit\":\"1\",\"symbol\":\"corner_limit_multiplier\"},{\"value\":152.02,\"unit\":\"kPa\",\"symbol\":\"R\"}],\"result\":{\"value\":228.03000000000003,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.26\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"formula\"},{\"step_id\":\"p_le_R\",\"expression\":\"p \\\\le R\",\"substitutions\":[{\"value\":120.0,\"unit\":\"kPa\",\"symbol\":\"p\"},{\"value\":152.02,\"unit\":\"kPa\",\"symbol\":\"R\"}],\"result\":{\"value\":120.0,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.7\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"check\",\"operator\":\"le\",\"right\":{\"value\":152.02,\"unit\":\"kPa\"},\"passed\":true},{\"step_id\":\"p_x_max_le_limit\",\"expression\":\"p_x_max \\\\le edge_limit\",\"substitutions\":[{\"value\":240.0,\"unit\":\"kPa\",\"symbol\":\"p_x_max\"},{\"value\":182.424,\"unit\":\"kPa\",\"symbol\":\"edge_limit\"}],\"result\":{\"value\":240.0,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.26\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"check\",\"operator\":\"le\",\"right\":{\"value\":182.424,\"unit\":\"kPa\"},\"passed\":false},{\"step_id\":\"p_y_max_le_limit\",\"expression\":\"p_y_max \\\\le edge_limit\",\"substitutions\":[{\"value\":120.0,\"unit\":\"kPa\",\"symbol\":\"p_y_max\"},{\"value\":182.424,\"unit\":\"kPa\",\"symbol\":\"edge_limit\"}],\"result\":{\"value\":120.0,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.26\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"check\",\"operator\":\"le\",\"right\":{\"value\":182.424,\"unit\":\"kPa\"},\"passed\":true},{\"step_id\":\"p_corner_max_le_limit\",\"expression\":\"p_corner_max \\\\le corner_limit\",\"substitutions\":[{\"value\":240.0,\"unit\":\"kPa\",\"symbol\":\"p_corner_max\"},{\"value\":228.03000000000003,\"unit\":\"kPa\",\"symbol\":\"corner_limit\"}],\"result\":{\"value\":240.0,\"unit\":\"kPa\"},\"norm_refs\":[{\"document\":\"СП 22.13330.2016\",\"edition\":\"2016 (с Изменениями N 1, 2, 3, 4, 5)\",\"clause\":\"5.6.26\",\"status\":\"unverified\",\"provenance\":\"machine-extracted\"}],\"kind\":\"check\",\"operator\":\"le\",\"right\":{\"value\":228.03000000000003,\"unit\":\"kPa\"},\"passed\":false}],\"unverified_step_count\":30,\"result_id\":\"bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb\",\"parameter_source\":{\"kind\":\"interim\",\"data_sha256\":\"faaa0724af57ca6c8066f558c4e75c2785d099b34cbfb07c4a85892fdc3b68fe\",\"profile\":\"strict\"}}"

export const loadsStrictSource = {
  "kind": "interim",
  "data_sha256": "faaa0724af57ca6c8066f558c4e75c2785d099b34cbfb07c4a85892fdc3b68fe", // pragma: allowlist secret
  "profile": "strict"
} satisfies ParameterSourceInfo

export const loadsDraftSource = {
  "kind": "interim",
  "data_sha256": "faaa0724af57ca6c8066f558c4e75c2785d099b34cbfb07c4a85892fdc3b68fe", // pragma: allowlist secret
  "profile": "draft"
} satisfies ParameterSourceInfo

export const loadsScenarios = [
  { name: 'Central', inputs: loadsCentralInputs, envelope: loadsCentralEnvelope, json: loadsCentralJson },
  { name: 'OneAxis', inputs: loadsOneAxisInputs, envelope: loadsOneAxisEnvelope, json: loadsOneAxisJson },
  { name: 'Biaxial', inputs: loadsBiaxialInputs, envelope: loadsBiaxialEnvelope, json: loadsBiaxialJson },
  { name: 'Fail', inputs: loadsFailInputs, envelope: loadsFailEnvelope, json: loadsFailJson },
  { name: 'BoundRefusal', inputs: loadsBoundRefusalInputs, envelope: loadsBoundRefusalEnvelope, json: loadsBoundRefusalJson },
  { name: 'ContactRefusal', inputs: loadsContactRefusalInputs, envelope: loadsContactRefusalEnvelope, json: loadsContactRefusalJson },
  { name: 'ZeroContact', inputs: loadsZeroContactInputs, envelope: loadsZeroContactEnvelope, json: loadsZeroContactJson },
]
