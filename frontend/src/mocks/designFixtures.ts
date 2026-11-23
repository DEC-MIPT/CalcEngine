import type { components } from '../api/schema'
export const weightsCalculationType = {
  "name": "foundations_shallow_weights",
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
        "ru": "Независимо от d_1; структурные моменты переносятся по M+Q*h",
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
    },
    {
      "name": "G_fund",
      "base_unit": "kN",
      "dimension": "force",
      "units": [
        "N",
        "kN",
        "MN"
      ],
      "label": {
        "ru": "Вес фундамента",
        "en": null
      },
      "symbol": "G_{fund}",
      "hint": {
        "ru": "Вниз, неотрицательный; не включать повторно в N",
        "en": null
      },
      "whole_values_only": false
    },
    {
      "name": "G_soil",
      "base_unit": "kN",
      "dimension": "force",
      "units": [
        "N",
        "kN",
        "MN"
      ],
      "label": {
        "ru": "Вес грунта над подошвой",
        "en": null
      },
      "symbol": "G_{soil}",
      "hint": {
        "ru": "Вниз, неотрицательный; для заданной геометрии",
        "en": null
      },
      "whole_values_only": false
    },
    {
      "name": "G_other",
      "base_unit": "kN",
      "dimension": "force",
      "units": [
        "N",
        "kN",
        "MN"
      ],
      "label": {
        "ru": "Прочие добавленные веса",
        "en": null
      },
      "symbol": "G_{other}",
      "hint": {
        "ru": "Вниз, неотрицательные; не включать повторно в N",
        "en": null
      },
      "whole_values_only": false
    },
    {
      "name": "Mx_add_base",
      "base_unit": "kN*m",
      "dimension": "moment",
      "units": [
        "N*m",
        "kN*m",
        "MN*m"
      ],
      "label": {
        "ru": "Дополнительный момент на подошве для давления вдоль x=b",
        "en": null
      },
      "symbol": "M_{x,add,base}",
      "hint": {
        "ru": "Подписанный; повторно через h не переносится",
        "en": null
      },
      "whole_values_only": false
    },
    {
      "name": "My_add_base",
      "base_unit": "kN*m",
      "dimension": "moment",
      "units": [
        "N*m",
        "kN*m",
        "MN*m"
      ],
      "label": {
        "ru": "Дополнительный момент на подошве для давления вдоль y=l",
        "en": null
      },
      "symbol": "M_{y,add,base}",
      "hint": {
        "ru": "Подписанный; повторно через h не переносится",
        "en": null
      },
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
} satisfies components['schemas']['CalculationTypeView']
export const weightsCentralRequest = {
  "calculation_type": "foundations_shallow_weights",
  "inputs": {
    "b": {
      "value": 2.0,
      "unit": "m"
    },
    "d_1": {
      "value": 1.0,
      "unit": "m"
    },
    "d_b": {
      "value": 0.0,
      "unit": "m"
    },
    "gamma_II": {
      "value": 20.0,
      "unit": "kN/m3"
    },
    "gamma_II_prime": {
      "value": 20.0,
      "unit": "kN/m3"
    },
    "c_II": {
      "value": 10.0,
      "unit": "kPa"
    },
    "phi_II": {
      "value": 20.0,
      "unit": "deg"
    },
    "l": {
      "value": 3.0,
      "unit": "m"
    },
    "h": {
      "value": 1.0,
      "unit": "m"
    },
    "N": {
      "value": 600.0,
      "unit": "kN"
    },
    "Mx": {
      "value": 0.0,
      "unit": "kN*m"
    },
    "My": {
      "value": 0.0,
      "unit": "kN*m"
    },
    "Qx": {
      "value": 0.0,
      "unit": "kN"
    },
    "Qy": {
      "value": 0.0,
      "unit": "kN"
    },
    "G_fund": {
      "value": 60.0,
      "unit": "kN"
    },
    "G_soil": {
      "value": 40.0,
      "unit": "kN"
    },
    "G_other": {
      "value": 20.0,
      "unit": "kN"
    },
    "Mx_add_base": {
      "value": 0.0,
      "unit": "kN*m"
    },
    "My_add_base": {
      "value": 0.0,
      "unit": "kN*m"
    }
  }
} satisfies components['schemas']['CalculationRequest']
export const weightsCentralEnvelope = {
  "engine_version": "0.1.0",
  "input_hash": "cddb43a0c5d4b22d026bb1f6404f5e641710447afc637ba63f0e4950af838733", // pragma: allowlist secret
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
      "rationale": "Явные веса: V=N+G_fund+G_soil+G_other; M_base=M+Q*h+M_add_base. Нагрузки конструкции на обрезе, дополнительные моменты на подошве; решение инженера 2026-11-22."
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
      "expression": "M_{x,base}=M_x+Q_x h+M_{x,add,base}",
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
        },
        {
          "value": 0.0,
          "unit": "kN*m",
          "symbol": "Mx_add_base"
        }
      ],
      "result": {
        "value": 0.0,
        "unit": "kN*m"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Явные веса: V=N+G_fund+G_soil+G_other; M_base=M+Q*h+M_add_base. Нагрузки конструкции на обрезе, дополнительные моменты на подошве; решение инженера 2026-11-22."
      }
    },
    {
      "kind": "engineer_formula",
      "step_id": "My_base",
      "expression": "M_{y,base}=M_y+Q_y h+M_{y,add,base}",
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
        },
        {
          "value": 0.0,
          "unit": "kN*m",
          "symbol": "My_add_base"
        }
      ],
      "result": {
        "value": 0.0,
        "unit": "kN*m"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Явные веса: V=N+G_fund+G_soil+G_other; M_base=M+Q*h+M_add_base. Нагрузки конструкции на обрезе, дополнительные моменты на подошве; решение инженера 2026-11-22."
      }
    },
    {
      "kind": "engineer_formula",
      "step_id": "G_sum",
      "expression": "G_{sum}=G_{fund}+G_{soil}+G_{other}",
      "substitutions": [
        {
          "value": 60.0,
          "unit": "kN",
          "symbol": "G_fund"
        },
        {
          "value": 40.0,
          "unit": "kN",
          "symbol": "G_soil"
        },
        {
          "value": 20.0,
          "unit": "kN",
          "symbol": "G_other"
        }
      ],
      "result": {
        "value": 120.0,
        "unit": "kN"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Явные веса: V=N+G_fund+G_soil+G_other; M_base=M+Q*h+M_add_base. Нагрузки конструкции на обрезе, дополнительные моменты на подошве; решение инженера 2026-11-22."
      }
    },
    {
      "kind": "engineer_formula",
      "step_id": "V",
      "expression": "V=N+G_{sum}",
      "substitutions": [
        {
          "value": 600.0,
          "unit": "kN",
          "symbol": "N"
        },
        {
          "value": 120.0,
          "unit": "kN",
          "symbol": "G_sum"
        }
      ],
      "result": {
        "value": 720.0,
        "unit": "kN"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Явные веса: V=N+G_fund+G_soil+G_other; M_base=M+Q*h+M_add_base. Нагрузки конструкции на обрезе, дополнительные моменты на подошве; решение инженера 2026-11-22."
      }
    },
    {
      "kind": "engineer_formula",
      "step_id": "p",
      "expression": "p=V/A",
      "substitutions": [
        {
          "value": 720.0,
          "unit": "kN",
          "symbol": "V"
        },
        {
          "value": 6.0,
          "unit": "m2",
          "symbol": "A"
        }
      ],
      "result": {
        "value": 120.0,
        "unit": "kPa"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Явные веса: V=N+G_fund+G_soil+G_other; M_base=M+Q*h+M_add_base. Нагрузки конструкции на обрезе, дополнительные моменты на подошве; решение инженера 2026-11-22."
      }
    },
    {
      "kind": "engineer_formula",
      "step_id": "p_x_min",
      "expression": "p_{x,min}=p-|M_{x,base}|/W_x",
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
        }
      ],
      "result": {
        "value": 120.0,
        "unit": "kPa"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Явные веса: V=N+G_fund+G_soil+G_other; M_base=M+Q*h+M_add_base. Нагрузки конструкции на обрезе, дополнительные моменты на подошве; решение инженера 2026-11-22."
      }
    },
    {
      "kind": "engineer_formula",
      "step_id": "p_x_max",
      "expression": "p_{x,max}=p+|M_{x,base}|/W_x",
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
        }
      ],
      "result": {
        "value": 120.0,
        "unit": "kPa"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Явные веса: V=N+G_fund+G_soil+G_other; M_base=M+Q*h+M_add_base. Нагрузки конструкции на обрезе, дополнительные моменты на подошве; решение инженера 2026-11-22."
      }
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
      "kind": "engineer_formula",
      "step_id": "p_y_min",
      "expression": "p_{y,min}=p-|M_{y,base}|/W_y",
      "substitutions": [
        {
          "value": 120.0,
          "unit": "kPa",
          "symbol": "p"
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
        }
      ],
      "result": {
        "value": 120.0,
        "unit": "kPa"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Явные веса: V=N+G_fund+G_soil+G_other; M_base=M+Q*h+M_add_base. Нагрузки конструкции на обрезе, дополнительные моменты на подошве; решение инженера 2026-11-22."
      }
    },
    {
      "kind": "engineer_formula",
      "step_id": "p_y_max",
      "expression": "p_{y,max}=p+|M_{y,base}|/W_y",
      "substitutions": [
        {
          "value": 120.0,
          "unit": "kPa",
          "symbol": "p"
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
        }
      ],
      "result": {
        "value": 120.0,
        "unit": "kPa"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Явные веса: V=N+G_fund+G_soil+G_other; M_base=M+Q*h+M_add_base. Нагрузки конструкции на обрезе, дополнительные моменты на подошве; решение инженера 2026-11-22."
      }
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
        }
      ],
      "result": {
        "value": 120.0,
        "unit": "kPa"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Явные веса: V=N+G_fund+G_soil+G_other; M_base=M+Q*h+M_add_base. Нагрузки конструкции на обрезе, дополнительные моменты на подошве; решение инженера 2026-11-22."
      }
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
        }
      ],
      "result": {
        "value": 120.0,
        "unit": "kPa"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Явные веса: V=N+G_fund+G_soil+G_other; M_base=M+Q*h+M_add_base. Нагрузки конструкции на обрезе, дополнительные моменты на подошве; решение инженера 2026-11-22."
      }
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
        }
      ],
      "result": {
        "value": 120.0,
        "unit": "kPa"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Явные веса: V=N+G_fund+G_soil+G_other; M_base=M+Q*h+M_add_base. Нагрузки конструкции на обрезе, дополнительные моменты на подошве; решение инженера 2026-11-22."
      }
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
        }
      ],
      "result": {
        "value": 120.0,
        "unit": "kPa"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Явные веса: V=N+G_fund+G_soil+G_other; M_base=M+Q*h+M_add_base. Нагрузки конструкции на обрезе, дополнительные моменты на подошве; решение инженера 2026-11-22."
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
  "unverified_step_count": 20,
  "result_id": "dec00000-0000-4000-8000-000000000001",
  "parameter_source": {
    "kind": "interim",
    "data_sha256": "faaa0724af57ca6c8066f558c4e75c2785d099b34cbfb07c4a85892fdc3b68fe", // pragma: allowlist secret
    "profile": "strict"
  }
} satisfies components['schemas']['ResultEnvelope']
export const weightsCentralContext = {
  "status": "available",
  "context": {
    "schema_version": "foundation-result-context-v1",
    "result_id": "dec00000-0000-4000-8000-000000000001",
    "calculation_type": "foundations_shallow_weights",
    "methodology_version": "rectangular-explicit-weights-v1",
    "input_hash": "cddb43a0c5d4b22d026bb1f6404f5e641710447afc637ba63f0e4950af838733", // pragma: allowlist secret
    "load_level": "upper_cut",
    "weight_mode": "explicit",
    "inputs": {
      "b": {
        "value": 2.0,
        "unit": "m"
      },
      "d_1": {
        "value": 1.0,
        "unit": "m"
      },
      "d_b": {
        "value": 0.0,
        "unit": "m"
      },
      "gamma_II": {
        "value": 20.0,
        "unit": "kN/m3"
      },
      "gamma_II_prime": {
        "value": 20.0,
        "unit": "kN/m3"
      },
      "c_II": {
        "value": 10.0,
        "unit": "kPa"
      },
      "phi_II": {
        "value": 20.0,
        "unit": "deg"
      },
      "l": {
        "value": 3.0,
        "unit": "m"
      },
      "h": {
        "value": 1.0,
        "unit": "m"
      },
      "N": {
        "value": 600.0,
        "unit": "kN"
      },
      "Mx": {
        "value": 0.0,
        "unit": "kN*m"
      },
      "My": {
        "value": 0.0,
        "unit": "kN*m"
      },
      "Qx": {
        "value": 0.0,
        "unit": "kN"
      },
      "Qy": {
        "value": 0.0,
        "unit": "kN"
      },
      "G_fund": {
        "value": 60.0,
        "unit": "kN"
      },
      "G_soil": {
        "value": 40.0,
        "unit": "kN"
      },
      "G_other": {
        "value": 20.0,
        "unit": "kN"
      },
      "Mx_add_base": {
        "value": 0.0,
        "unit": "kN*m"
      },
      "My_add_base": {
        "value": 0.0,
        "unit": "kN*m"
      }
    },
    "geometry": {
      "b": {
        "value": 2.0,
        "unit": "m"
      },
      "l": {
        "value": 3.0,
        "unit": "m"
      },
      "A": {
        "value": 6.0,
        "unit": "m2"
      },
      "Wx": {
        "value": 2.0,
        "unit": "m3"
      },
      "Wy": {
        "value": 3.0,
        "unit": "m3"
      }
    },
    "trace_values": {
      "gamma_c1": {
        "value": 1.1,
        "unit": "1"
      },
      "gamma_c2": {
        "value": 1.0,
        "unit": "1"
      },
      "k": {
        "value": 1.0,
        "unit": "1"
      },
      "M_gamma": {
        "value": 0.51,
        "unit": "1"
      },
      "M_q": {
        "value": 3.06,
        "unit": "1"
      },
      "M_c": {
        "value": 5.66,
        "unit": "1"
      },
      "k_z": {
        "value": 1.0,
        "unit": "1"
      },
      "R": {
        "value": 152.02,
        "unit": "kPa"
      },
      "A": {
        "value": 6.0,
        "unit": "m2"
      },
      "Wx": {
        "value": 2.0,
        "unit": "m3"
      },
      "Wy": {
        "value": 3.0,
        "unit": "m3"
      },
      "Mx_base": {
        "value": 0.0,
        "unit": "kN*m"
      },
      "My_base": {
        "value": 0.0,
        "unit": "kN*m"
      },
      "G_sum": {
        "value": 120.0,
        "unit": "kN"
      },
      "V": {
        "value": 720.0,
        "unit": "kN"
      },
      "p": {
        "value": 120.0,
        "unit": "kPa"
      },
      "p_x_min": {
        "value": 120.0,
        "unit": "kPa"
      },
      "p_x_max": {
        "value": 120.0,
        "unit": "kPa"
      },
      "e_x": {
        "value": 0.0,
        "unit": "m"
      },
      "relative_eccentricity_x": {
        "value": 1.0,
        "unit": "1"
      },
      "pressure_diagram_x": {
        "value": 0.0,
        "unit": "m"
      },
      "p_y_min": {
        "value": 120.0,
        "unit": "kPa"
      },
      "p_y_max": {
        "value": 120.0,
        "unit": "kPa"
      },
      "e_y": {
        "value": 0.0,
        "unit": "m"
      },
      "relative_eccentricity_y": {
        "value": 1.0,
        "unit": "1"
      },
      "pressure_diagram_y": {
        "value": 0.0,
        "unit": "m"
      },
      "p_corner_pp": {
        "value": 120.0,
        "unit": "kPa"
      },
      "p_corner_pm": {
        "value": 120.0,
        "unit": "kPa"
      },
      "p_corner_mp": {
        "value": 120.0,
        "unit": "kPa"
      },
      "p_corner_mm": {
        "value": 120.0,
        "unit": "kPa"
      },
      "p_corner_min": {
        "value": 120.0,
        "unit": "kPa"
      },
      "p_corner_max": {
        "value": 120.0,
        "unit": "kPa"
      },
      "edge_limit_multiplier": {
        "value": 1.2,
        "unit": "1"
      },
      "edge_limit": {
        "value": 182.424,
        "unit": "kPa"
      },
      "corner_limit_multiplier": {
        "value": 1.5,
        "unit": "1"
      },
      "corner_limit": {
        "value": 228.03000000000003,
        "unit": "kPa"
      },
      "p_le_R": {
        "value": 120.0,
        "unit": "kPa"
      },
      "p_x_max_le_limit": {
        "value": 120.0,
        "unit": "kPa"
      },
      "p_y_max_le_limit": {
        "value": 120.0,
        "unit": "kPa"
      },
      "p_corner_max_le_limit": {
        "value": 120.0,
        "unit": "kPa"
      }
    },
    "pressure_state": "full_contact",
    "corners": [
      {
        "name": "pp",
        "x": {
          "value": 1.0,
          "unit": "m"
        },
        "y": {
          "value": 1.5,
          "unit": "m"
        },
        "pressure": {
          "value": 120.0,
          "unit": "kPa"
        },
        "step_id": "p_corner_pp"
      },
      {
        "name": "pm",
        "x": {
          "value": 1.0,
          "unit": "m"
        },
        "y": {
          "value": -1.5,
          "unit": "m"
        },
        "pressure": {
          "value": 120.0,
          "unit": "kPa"
        },
        "step_id": "p_corner_pm"
      },
      {
        "name": "mp",
        "x": {
          "value": -1.0,
          "unit": "m"
        },
        "y": {
          "value": 1.5,
          "unit": "m"
        },
        "pressure": {
          "value": 120.0,
          "unit": "kPa"
        },
        "step_id": "p_corner_mp"
      },
      {
        "name": "mm",
        "x": {
          "value": -1.0,
          "unit": "m"
        },
        "y": {
          "value": -1.5,
          "unit": "m"
        },
        "pressure": {
          "value": 120.0,
          "unit": "kPa"
        },
        "step_id": "p_corner_mm"
      }
    ]
  }
} satisfies components['schemas']['FoundationContextResponse']
export const weightsOneAxisRequest = {
  "calculation_type": "foundations_shallow_weights",
  "inputs": {
    "b": {
      "value": 2.0,
      "unit": "m"
    },
    "d_1": {
      "value": 1.0,
      "unit": "m"
    },
    "d_b": {
      "value": 0.0,
      "unit": "m"
    },
    "gamma_II": {
      "value": 20.0,
      "unit": "kN/m3"
    },
    "gamma_II_prime": {
      "value": 20.0,
      "unit": "kN/m3"
    },
    "c_II": {
      "value": 10.0,
      "unit": "kPa"
    },
    "phi_II": {
      "value": 20.0,
      "unit": "deg"
    },
    "l": {
      "value": 3.0,
      "unit": "m"
    },
    "h": {
      "value": 1.0,
      "unit": "m"
    },
    "N": {
      "value": 600.0,
      "unit": "kN"
    },
    "Mx": {
      "value": 40.0,
      "unit": "kN*m"
    },
    "My": {
      "value": 0.0,
      "unit": "kN*m"
    },
    "Qx": {
      "value": 20.0,
      "unit": "kN"
    },
    "Qy": {
      "value": 0.0,
      "unit": "kN"
    },
    "G_fund": {
      "value": 60.0,
      "unit": "kN"
    },
    "G_soil": {
      "value": 40.0,
      "unit": "kN"
    },
    "G_other": {
      "value": 50.0,
      "unit": "kN"
    },
    "Mx_add_base": {
      "value": 10.0,
      "unit": "kN*m"
    },
    "My_add_base": {
      "value": 0.0,
      "unit": "kN*m"
    }
  }
} satisfies components['schemas']['CalculationRequest']
export const weightsOneAxisEnvelope = {
  "engine_version": "0.1.0",
  "input_hash": "6772e307e9fd69d2760e1f3c457de3b585db9c5a85840d7363ebdf99beee0171", // pragma: allowlist secret
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
      "value": 125.0,
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
      "value": 160.0,
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
      "value": 125.0,
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
      "value": 125.0,
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
      "value": 160.0,
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
      "value": 160.0,
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
      "rationale": "Явные веса: V=N+G_fund+G_soil+G_other; M_base=M+Q*h+M_add_base. Нагрузки конструкции на обрезе, дополнительные моменты на подошве; решение инженера 2026-11-22."
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
      "expression": "M_{x,base}=M_x+Q_x h+M_{x,add,base}",
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
        },
        {
          "value": 10.0,
          "unit": "kN*m",
          "symbol": "Mx_add_base"
        }
      ],
      "result": {
        "value": 70.0,
        "unit": "kN*m"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Явные веса: V=N+G_fund+G_soil+G_other; M_base=M+Q*h+M_add_base. Нагрузки конструкции на обрезе, дополнительные моменты на подошве; решение инженера 2026-11-22."
      }
    },
    {
      "kind": "engineer_formula",
      "step_id": "My_base",
      "expression": "M_{y,base}=M_y+Q_y h+M_{y,add,base}",
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
        },
        {
          "value": 0.0,
          "unit": "kN*m",
          "symbol": "My_add_base"
        }
      ],
      "result": {
        "value": 0.0,
        "unit": "kN*m"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Явные веса: V=N+G_fund+G_soil+G_other; M_base=M+Q*h+M_add_base. Нагрузки конструкции на обрезе, дополнительные моменты на подошве; решение инженера 2026-11-22."
      }
    },
    {
      "kind": "engineer_formula",
      "step_id": "G_sum",
      "expression": "G_{sum}=G_{fund}+G_{soil}+G_{other}",
      "substitutions": [
        {
          "value": 60.0,
          "unit": "kN",
          "symbol": "G_fund"
        },
        {
          "value": 40.0,
          "unit": "kN",
          "symbol": "G_soil"
        },
        {
          "value": 50.0,
          "unit": "kN",
          "symbol": "G_other"
        }
      ],
      "result": {
        "value": 150.0,
        "unit": "kN"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Явные веса: V=N+G_fund+G_soil+G_other; M_base=M+Q*h+M_add_base. Нагрузки конструкции на обрезе, дополнительные моменты на подошве; решение инженера 2026-11-22."
      }
    },
    {
      "kind": "engineer_formula",
      "step_id": "V",
      "expression": "V=N+G_{sum}",
      "substitutions": [
        {
          "value": 600.0,
          "unit": "kN",
          "symbol": "N"
        },
        {
          "value": 150.0,
          "unit": "kN",
          "symbol": "G_sum"
        }
      ],
      "result": {
        "value": 750.0,
        "unit": "kN"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Явные веса: V=N+G_fund+G_soil+G_other; M_base=M+Q*h+M_add_base. Нагрузки конструкции на обрезе, дополнительные моменты на подошве; решение инженера 2026-11-22."
      }
    },
    {
      "kind": "engineer_formula",
      "step_id": "p",
      "expression": "p=V/A",
      "substitutions": [
        {
          "value": 750.0,
          "unit": "kN",
          "symbol": "V"
        },
        {
          "value": 6.0,
          "unit": "m2",
          "symbol": "A"
        }
      ],
      "result": {
        "value": 125.0,
        "unit": "kPa"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Явные веса: V=N+G_fund+G_soil+G_other; M_base=M+Q*h+M_add_base. Нагрузки конструкции на обрезе, дополнительные моменты на подошве; решение инженера 2026-11-22."
      }
    },
    {
      "kind": "engineer_formula",
      "step_id": "p_x_min",
      "expression": "p_{x,min}=p-|M_{x,base}|/W_x",
      "substitutions": [
        {
          "value": 125.0,
          "unit": "kPa",
          "symbol": "p"
        },
        {
          "value": 70.0,
          "unit": "kN*m",
          "symbol": "Mx_base"
        },
        {
          "value": 2.0,
          "unit": "m3",
          "symbol": "Wx"
        }
      ],
      "result": {
        "value": 90.0,
        "unit": "kPa"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Явные веса: V=N+G_fund+G_soil+G_other; M_base=M+Q*h+M_add_base. Нагрузки конструкции на обрезе, дополнительные моменты на подошве; решение инженера 2026-11-22."
      }
    },
    {
      "kind": "engineer_formula",
      "step_id": "p_x_max",
      "expression": "p_{x,max}=p+|M_{x,base}|/W_x",
      "substitutions": [
        {
          "value": 125.0,
          "unit": "kPa",
          "symbol": "p"
        },
        {
          "value": 70.0,
          "unit": "kN*m",
          "symbol": "Mx_base"
        },
        {
          "value": 2.0,
          "unit": "m3",
          "symbol": "Wx"
        }
      ],
      "result": {
        "value": 160.0,
        "unit": "kPa"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Явные веса: V=N+G_fund+G_soil+G_other; M_base=M+Q*h+M_add_base. Нагрузки конструкции на обрезе, дополнительные моменты на подошве; решение инженера 2026-11-22."
      }
    },
    {
      "kind": "engineer_formula",
      "step_id": "e_x",
      "expression": "e_x=|M_{x,base}|/V",
      "substitutions": [
        {
          "value": 70.0,
          "unit": "kN*m",
          "symbol": "Mx_base"
        },
        {
          "value": 750.0,
          "unit": "kN",
          "symbol": "V"
        }
      ],
      "result": {
        "value": 0.09333333333333334,
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
          "value": 0.04666666666666667,
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
          "value": 0.09333333333333334,
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
        "value": 0.09333333333333334,
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
      "kind": "engineer_formula",
      "step_id": "p_y_min",
      "expression": "p_{y,min}=p-|M_{y,base}|/W_y",
      "substitutions": [
        {
          "value": 125.0,
          "unit": "kPa",
          "symbol": "p"
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
        }
      ],
      "result": {
        "value": 125.0,
        "unit": "kPa"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Явные веса: V=N+G_fund+G_soil+G_other; M_base=M+Q*h+M_add_base. Нагрузки конструкции на обрезе, дополнительные моменты на подошве; решение инженера 2026-11-22."
      }
    },
    {
      "kind": "engineer_formula",
      "step_id": "p_y_max",
      "expression": "p_{y,max}=p+|M_{y,base}|/W_y",
      "substitutions": [
        {
          "value": 125.0,
          "unit": "kPa",
          "symbol": "p"
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
        }
      ],
      "result": {
        "value": 125.0,
        "unit": "kPa"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Явные веса: V=N+G_fund+G_soil+G_other; M_base=M+Q*h+M_add_base. Нагрузки конструкции на обрезе, дополнительные моменты на подошве; решение инженера 2026-11-22."
      }
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
          "value": 750.0,
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
      "kind": "engineer_formula",
      "step_id": "p_corner_pp",
      "expression": "p_{pp}=p+s_x M_{x,base}/W_x+s_y M_{y,base}/W_y",
      "substitutions": [
        {
          "value": 125.0,
          "unit": "kPa",
          "symbol": "p"
        },
        {
          "value": 70.0,
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
        }
      ],
      "result": {
        "value": 160.0,
        "unit": "kPa"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Явные веса: V=N+G_fund+G_soil+G_other; M_base=M+Q*h+M_add_base. Нагрузки конструкции на обрезе, дополнительные моменты на подошве; решение инженера 2026-11-22."
      }
    },
    {
      "kind": "engineer_formula",
      "step_id": "p_corner_pm",
      "expression": "p_{pm}=p+s_x M_{x,base}/W_x+s_y M_{y,base}/W_y",
      "substitutions": [
        {
          "value": 125.0,
          "unit": "kPa",
          "symbol": "p"
        },
        {
          "value": 70.0,
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
        }
      ],
      "result": {
        "value": 160.0,
        "unit": "kPa"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Явные веса: V=N+G_fund+G_soil+G_other; M_base=M+Q*h+M_add_base. Нагрузки конструкции на обрезе, дополнительные моменты на подошве; решение инженера 2026-11-22."
      }
    },
    {
      "kind": "engineer_formula",
      "step_id": "p_corner_mp",
      "expression": "p_{mp}=p+s_x M_{x,base}/W_x+s_y M_{y,base}/W_y",
      "substitutions": [
        {
          "value": 125.0,
          "unit": "kPa",
          "symbol": "p"
        },
        {
          "value": 70.0,
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
        }
      ],
      "result": {
        "value": 90.0,
        "unit": "kPa"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Явные веса: V=N+G_fund+G_soil+G_other; M_base=M+Q*h+M_add_base. Нагрузки конструкции на обрезе, дополнительные моменты на подошве; решение инженера 2026-11-22."
      }
    },
    {
      "kind": "engineer_formula",
      "step_id": "p_corner_mm",
      "expression": "p_{mm}=p+s_x M_{x,base}/W_x+s_y M_{y,base}/W_y",
      "substitutions": [
        {
          "value": 125.0,
          "unit": "kPa",
          "symbol": "p"
        },
        {
          "value": 70.0,
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
        }
      ],
      "result": {
        "value": 90.0,
        "unit": "kPa"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Явные веса: V=N+G_fund+G_soil+G_other; M_base=M+Q*h+M_add_base. Нагрузки конструкции на обрезе, дополнительные моменты на подошве; решение инженера 2026-11-22."
      }
    },
    {
      "kind": "engineer_formula",
      "step_id": "p_corner_min",
      "expression": "p_{corner,min}=\\min(p_{++},p_{+-},p_{-+},p_{--})",
      "substitutions": [
        {
          "value": 160.0,
          "unit": "kPa",
          "symbol": "p_corner_pp"
        },
        {
          "value": 160.0,
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
          "value": 160.0,
          "unit": "kPa",
          "symbol": "p_corner_pp"
        },
        {
          "value": 160.0,
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
        "value": 160.0,
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
          "value": 125.0,
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
        "value": 125.0,
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
          "value": 160.0,
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
        "value": 160.0,
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
          "value": 125.0,
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
        "value": 125.0,
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
          "value": 160.0,
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
        "value": 160.0,
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
  "unverified_step_count": 20,
  "result_id": "dec00000-0000-4000-8000-000000000002",
  "parameter_source": {
    "kind": "interim",
    "data_sha256": "faaa0724af57ca6c8066f558c4e75c2785d099b34cbfb07c4a85892fdc3b68fe", // pragma: allowlist secret
    "profile": "strict"
  }
} satisfies components['schemas']['ResultEnvelope']
export const weightsOneAxisContext = {
  "status": "available",
  "context": {
    "schema_version": "foundation-result-context-v1",
    "result_id": "dec00000-0000-4000-8000-000000000002",
    "calculation_type": "foundations_shallow_weights",
    "methodology_version": "rectangular-explicit-weights-v1",
    "input_hash": "6772e307e9fd69d2760e1f3c457de3b585db9c5a85840d7363ebdf99beee0171", // pragma: allowlist secret
    "load_level": "upper_cut",
    "weight_mode": "explicit",
    "inputs": {
      "b": {
        "value": 2.0,
        "unit": "m"
      },
      "d_1": {
        "value": 1.0,
        "unit": "m"
      },
      "d_b": {
        "value": 0.0,
        "unit": "m"
      },
      "gamma_II": {
        "value": 20.0,
        "unit": "kN/m3"
      },
      "gamma_II_prime": {
        "value": 20.0,
        "unit": "kN/m3"
      },
      "c_II": {
        "value": 10.0,
        "unit": "kPa"
      },
      "phi_II": {
        "value": 20.0,
        "unit": "deg"
      },
      "l": {
        "value": 3.0,
        "unit": "m"
      },
      "h": {
        "value": 1.0,
        "unit": "m"
      },
      "N": {
        "value": 600.0,
        "unit": "kN"
      },
      "Mx": {
        "value": 40.0,
        "unit": "kN*m"
      },
      "My": {
        "value": 0.0,
        "unit": "kN*m"
      },
      "Qx": {
        "value": 20.0,
        "unit": "kN"
      },
      "Qy": {
        "value": 0.0,
        "unit": "kN"
      },
      "G_fund": {
        "value": 60.0,
        "unit": "kN"
      },
      "G_soil": {
        "value": 40.0,
        "unit": "kN"
      },
      "G_other": {
        "value": 50.0,
        "unit": "kN"
      },
      "Mx_add_base": {
        "value": 10.0,
        "unit": "kN*m"
      },
      "My_add_base": {
        "value": 0.0,
        "unit": "kN*m"
      }
    },
    "geometry": {
      "b": {
        "value": 2.0,
        "unit": "m"
      },
      "l": {
        "value": 3.0,
        "unit": "m"
      },
      "A": {
        "value": 6.0,
        "unit": "m2"
      },
      "Wx": {
        "value": 2.0,
        "unit": "m3"
      },
      "Wy": {
        "value": 3.0,
        "unit": "m3"
      }
    },
    "trace_values": {
      "gamma_c1": {
        "value": 1.1,
        "unit": "1"
      },
      "gamma_c2": {
        "value": 1.0,
        "unit": "1"
      },
      "k": {
        "value": 1.0,
        "unit": "1"
      },
      "M_gamma": {
        "value": 0.51,
        "unit": "1"
      },
      "M_q": {
        "value": 3.06,
        "unit": "1"
      },
      "M_c": {
        "value": 5.66,
        "unit": "1"
      },
      "k_z": {
        "value": 1.0,
        "unit": "1"
      },
      "R": {
        "value": 152.02,
        "unit": "kPa"
      },
      "A": {
        "value": 6.0,
        "unit": "m2"
      },
      "Wx": {
        "value": 2.0,
        "unit": "m3"
      },
      "Wy": {
        "value": 3.0,
        "unit": "m3"
      },
      "Mx_base": {
        "value": 70.0,
        "unit": "kN*m"
      },
      "My_base": {
        "value": 0.0,
        "unit": "kN*m"
      },
      "G_sum": {
        "value": 150.0,
        "unit": "kN"
      },
      "V": {
        "value": 750.0,
        "unit": "kN"
      },
      "p": {
        "value": 125.0,
        "unit": "kPa"
      },
      "p_x_min": {
        "value": 90.0,
        "unit": "kPa"
      },
      "p_x_max": {
        "value": 160.0,
        "unit": "kPa"
      },
      "e_x": {
        "value": 0.09333333333333334,
        "unit": "m"
      },
      "relative_eccentricity_x": {
        "value": 1.0,
        "unit": "1"
      },
      "pressure_diagram_x": {
        "value": 0.09333333333333334,
        "unit": "m"
      },
      "p_y_min": {
        "value": 125.0,
        "unit": "kPa"
      },
      "p_y_max": {
        "value": 125.0,
        "unit": "kPa"
      },
      "e_y": {
        "value": 0.0,
        "unit": "m"
      },
      "relative_eccentricity_y": {
        "value": 1.0,
        "unit": "1"
      },
      "pressure_diagram_y": {
        "value": 0.0,
        "unit": "m"
      },
      "p_corner_pp": {
        "value": 160.0,
        "unit": "kPa"
      },
      "p_corner_pm": {
        "value": 160.0,
        "unit": "kPa"
      },
      "p_corner_mp": {
        "value": 90.0,
        "unit": "kPa"
      },
      "p_corner_mm": {
        "value": 90.0,
        "unit": "kPa"
      },
      "p_corner_min": {
        "value": 90.0,
        "unit": "kPa"
      },
      "p_corner_max": {
        "value": 160.0,
        "unit": "kPa"
      },
      "edge_limit_multiplier": {
        "value": 1.2,
        "unit": "1"
      },
      "edge_limit": {
        "value": 182.424,
        "unit": "kPa"
      },
      "corner_limit_multiplier": {
        "value": 1.5,
        "unit": "1"
      },
      "corner_limit": {
        "value": 228.03000000000003,
        "unit": "kPa"
      },
      "p_le_R": {
        "value": 125.0,
        "unit": "kPa"
      },
      "p_x_max_le_limit": {
        "value": 160.0,
        "unit": "kPa"
      },
      "p_y_max_le_limit": {
        "value": 125.0,
        "unit": "kPa"
      },
      "p_corner_max_le_limit": {
        "value": 160.0,
        "unit": "kPa"
      }
    },
    "pressure_state": "full_contact",
    "corners": [
      {
        "name": "pp",
        "x": {
          "value": 1.0,
          "unit": "m"
        },
        "y": {
          "value": 1.5,
          "unit": "m"
        },
        "pressure": {
          "value": 160.0,
          "unit": "kPa"
        },
        "step_id": "p_corner_pp"
      },
      {
        "name": "pm",
        "x": {
          "value": 1.0,
          "unit": "m"
        },
        "y": {
          "value": -1.5,
          "unit": "m"
        },
        "pressure": {
          "value": 160.0,
          "unit": "kPa"
        },
        "step_id": "p_corner_pm"
      },
      {
        "name": "mp",
        "x": {
          "value": -1.0,
          "unit": "m"
        },
        "y": {
          "value": 1.5,
          "unit": "m"
        },
        "pressure": {
          "value": 90.0,
          "unit": "kPa"
        },
        "step_id": "p_corner_mp"
      },
      {
        "name": "mm",
        "x": {
          "value": -1.0,
          "unit": "m"
        },
        "y": {
          "value": -1.5,
          "unit": "m"
        },
        "pressure": {
          "value": 90.0,
          "unit": "kPa"
        },
        "step_id": "p_corner_mm"
      }
    ]
  }
} satisfies components['schemas']['FoundationContextResponse']
export const weightsBiaxialRequest = {
  "calculation_type": "foundations_shallow_weights",
  "inputs": {
    "b": {
      "value": 2.0,
      "unit": "m"
    },
    "d_1": {
      "value": 1.0,
      "unit": "m"
    },
    "d_b": {
      "value": 0.0,
      "unit": "m"
    },
    "gamma_II": {
      "value": 20.0,
      "unit": "kN/m3"
    },
    "gamma_II_prime": {
      "value": 20.0,
      "unit": "kN/m3"
    },
    "c_II": {
      "value": 10.0,
      "unit": "kPa"
    },
    "phi_II": {
      "value": 20.0,
      "unit": "deg"
    },
    "l": {
      "value": 3.0,
      "unit": "m"
    },
    "h": {
      "value": 1.0,
      "unit": "m"
    },
    "N": {
      "value": 600.0,
      "unit": "kN"
    },
    "Mx": {
      "value": 40.0,
      "unit": "kN*m"
    },
    "My": {
      "value": -30.0,
      "unit": "kN*m"
    },
    "Qx": {
      "value": 20.0,
      "unit": "kN"
    },
    "Qy": {
      "value": -15.0,
      "unit": "kN"
    },
    "G_fund": {
      "value": 60.0,
      "unit": "kN"
    },
    "G_soil": {
      "value": 40.0,
      "unit": "kN"
    },
    "G_other": {
      "value": 50.0,
      "unit": "kN"
    },
    "Mx_add_base": {
      "value": 10.0,
      "unit": "kN*m"
    },
    "My_add_base": {
      "value": -15.0,
      "unit": "kN*m"
    }
  }
} satisfies components['schemas']['CalculationRequest']
export const weightsBiaxialEnvelope = {
  "engine_version": "0.1.0",
  "input_hash": "afd729fb2996b377bb3761eb2e95a21df256a5461a07974cb01d9ba2f4de59a3", // pragma: allowlist secret
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
      "value": 125.0,
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
      "value": 160.0,
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
      "value": 145.0,
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
      "value": 140.0,
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
      "value": 180.0,
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
      "value": 70.0,
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
      "value": 110.0,
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
      "rationale": "Явные веса: V=N+G_fund+G_soil+G_other; M_base=M+Q*h+M_add_base. Нагрузки конструкции на обрезе, дополнительные моменты на подошве; решение инженера 2026-11-22."
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
      "expression": "M_{x,base}=M_x+Q_x h+M_{x,add,base}",
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
        },
        {
          "value": 10.0,
          "unit": "kN*m",
          "symbol": "Mx_add_base"
        }
      ],
      "result": {
        "value": 70.0,
        "unit": "kN*m"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Явные веса: V=N+G_fund+G_soil+G_other; M_base=M+Q*h+M_add_base. Нагрузки конструкции на обрезе, дополнительные моменты на подошве; решение инженера 2026-11-22."
      }
    },
    {
      "kind": "engineer_formula",
      "step_id": "My_base",
      "expression": "M_{y,base}=M_y+Q_y h+M_{y,add,base}",
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
        },
        {
          "value": -15.0,
          "unit": "kN*m",
          "symbol": "My_add_base"
        }
      ],
      "result": {
        "value": -60.0,
        "unit": "kN*m"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Явные веса: V=N+G_fund+G_soil+G_other; M_base=M+Q*h+M_add_base. Нагрузки конструкции на обрезе, дополнительные моменты на подошве; решение инженера 2026-11-22."
      }
    },
    {
      "kind": "engineer_formula",
      "step_id": "G_sum",
      "expression": "G_{sum}=G_{fund}+G_{soil}+G_{other}",
      "substitutions": [
        {
          "value": 60.0,
          "unit": "kN",
          "symbol": "G_fund"
        },
        {
          "value": 40.0,
          "unit": "kN",
          "symbol": "G_soil"
        },
        {
          "value": 50.0,
          "unit": "kN",
          "symbol": "G_other"
        }
      ],
      "result": {
        "value": 150.0,
        "unit": "kN"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Явные веса: V=N+G_fund+G_soil+G_other; M_base=M+Q*h+M_add_base. Нагрузки конструкции на обрезе, дополнительные моменты на подошве; решение инженера 2026-11-22."
      }
    },
    {
      "kind": "engineer_formula",
      "step_id": "V",
      "expression": "V=N+G_{sum}",
      "substitutions": [
        {
          "value": 600.0,
          "unit": "kN",
          "symbol": "N"
        },
        {
          "value": 150.0,
          "unit": "kN",
          "symbol": "G_sum"
        }
      ],
      "result": {
        "value": 750.0,
        "unit": "kN"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Явные веса: V=N+G_fund+G_soil+G_other; M_base=M+Q*h+M_add_base. Нагрузки конструкции на обрезе, дополнительные моменты на подошве; решение инженера 2026-11-22."
      }
    },
    {
      "kind": "engineer_formula",
      "step_id": "p",
      "expression": "p=V/A",
      "substitutions": [
        {
          "value": 750.0,
          "unit": "kN",
          "symbol": "V"
        },
        {
          "value": 6.0,
          "unit": "m2",
          "symbol": "A"
        }
      ],
      "result": {
        "value": 125.0,
        "unit": "kPa"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Явные веса: V=N+G_fund+G_soil+G_other; M_base=M+Q*h+M_add_base. Нагрузки конструкции на обрезе, дополнительные моменты на подошве; решение инженера 2026-11-22."
      }
    },
    {
      "kind": "engineer_formula",
      "step_id": "p_x_min",
      "expression": "p_{x,min}=p-|M_{x,base}|/W_x",
      "substitutions": [
        {
          "value": 125.0,
          "unit": "kPa",
          "symbol": "p"
        },
        {
          "value": 70.0,
          "unit": "kN*m",
          "symbol": "Mx_base"
        },
        {
          "value": 2.0,
          "unit": "m3",
          "symbol": "Wx"
        }
      ],
      "result": {
        "value": 90.0,
        "unit": "kPa"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Явные веса: V=N+G_fund+G_soil+G_other; M_base=M+Q*h+M_add_base. Нагрузки конструкции на обрезе, дополнительные моменты на подошве; решение инженера 2026-11-22."
      }
    },
    {
      "kind": "engineer_formula",
      "step_id": "p_x_max",
      "expression": "p_{x,max}=p+|M_{x,base}|/W_x",
      "substitutions": [
        {
          "value": 125.0,
          "unit": "kPa",
          "symbol": "p"
        },
        {
          "value": 70.0,
          "unit": "kN*m",
          "symbol": "Mx_base"
        },
        {
          "value": 2.0,
          "unit": "m3",
          "symbol": "Wx"
        }
      ],
      "result": {
        "value": 160.0,
        "unit": "kPa"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Явные веса: V=N+G_fund+G_soil+G_other; M_base=M+Q*h+M_add_base. Нагрузки конструкции на обрезе, дополнительные моменты на подошве; решение инженера 2026-11-22."
      }
    },
    {
      "kind": "engineer_formula",
      "step_id": "e_x",
      "expression": "e_x=|M_{x,base}|/V",
      "substitutions": [
        {
          "value": 70.0,
          "unit": "kN*m",
          "symbol": "Mx_base"
        },
        {
          "value": 750.0,
          "unit": "kN",
          "symbol": "V"
        }
      ],
      "result": {
        "value": 0.09333333333333334,
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
          "value": 0.04666666666666667,
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
          "value": 0.09333333333333334,
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
        "value": 0.09333333333333334,
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
      "kind": "engineer_formula",
      "step_id": "p_y_min",
      "expression": "p_{y,min}=p-|M_{y,base}|/W_y",
      "substitutions": [
        {
          "value": 125.0,
          "unit": "kPa",
          "symbol": "p"
        },
        {
          "value": -60.0,
          "unit": "kN*m",
          "symbol": "My_base"
        },
        {
          "value": 3.0,
          "unit": "m3",
          "symbol": "Wy"
        }
      ],
      "result": {
        "value": 105.0,
        "unit": "kPa"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Явные веса: V=N+G_fund+G_soil+G_other; M_base=M+Q*h+M_add_base. Нагрузки конструкции на обрезе, дополнительные моменты на подошве; решение инженера 2026-11-22."
      }
    },
    {
      "kind": "engineer_formula",
      "step_id": "p_y_max",
      "expression": "p_{y,max}=p+|M_{y,base}|/W_y",
      "substitutions": [
        {
          "value": 125.0,
          "unit": "kPa",
          "symbol": "p"
        },
        {
          "value": -60.0,
          "unit": "kN*m",
          "symbol": "My_base"
        },
        {
          "value": 3.0,
          "unit": "m3",
          "symbol": "Wy"
        }
      ],
      "result": {
        "value": 145.0,
        "unit": "kPa"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Явные веса: V=N+G_fund+G_soil+G_other; M_base=M+Q*h+M_add_base. Нагрузки конструкции на обрезе, дополнительные моменты на подошве; решение инженера 2026-11-22."
      }
    },
    {
      "kind": "engineer_formula",
      "step_id": "e_y",
      "expression": "e_y=|M_{y,base}|/V",
      "substitutions": [
        {
          "value": -60.0,
          "unit": "kN*m",
          "symbol": "My_base"
        },
        {
          "value": 750.0,
          "unit": "kN",
          "symbol": "V"
        }
      ],
      "result": {
        "value": 0.08,
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
          "value": 0.02666666666666667,
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
          "value": 0.08,
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
        "value": 0.08,
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
      "kind": "engineer_formula",
      "step_id": "p_corner_pp",
      "expression": "p_{pp}=p+s_x M_{x,base}/W_x+s_y M_{y,base}/W_y",
      "substitutions": [
        {
          "value": 125.0,
          "unit": "kPa",
          "symbol": "p"
        },
        {
          "value": 70.0,
          "unit": "kN*m",
          "symbol": "Mx_base"
        },
        {
          "value": 2.0,
          "unit": "m3",
          "symbol": "Wx"
        },
        {
          "value": -60.0,
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
        }
      ],
      "result": {
        "value": 140.0,
        "unit": "kPa"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Явные веса: V=N+G_fund+G_soil+G_other; M_base=M+Q*h+M_add_base. Нагрузки конструкции на обрезе, дополнительные моменты на подошве; решение инженера 2026-11-22."
      }
    },
    {
      "kind": "engineer_formula",
      "step_id": "p_corner_pm",
      "expression": "p_{pm}=p+s_x M_{x,base}/W_x+s_y M_{y,base}/W_y",
      "substitutions": [
        {
          "value": 125.0,
          "unit": "kPa",
          "symbol": "p"
        },
        {
          "value": 70.0,
          "unit": "kN*m",
          "symbol": "Mx_base"
        },
        {
          "value": 2.0,
          "unit": "m3",
          "symbol": "Wx"
        },
        {
          "value": -60.0,
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
        }
      ],
      "result": {
        "value": 180.0,
        "unit": "kPa"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Явные веса: V=N+G_fund+G_soil+G_other; M_base=M+Q*h+M_add_base. Нагрузки конструкции на обрезе, дополнительные моменты на подошве; решение инженера 2026-11-22."
      }
    },
    {
      "kind": "engineer_formula",
      "step_id": "p_corner_mp",
      "expression": "p_{mp}=p+s_x M_{x,base}/W_x+s_y M_{y,base}/W_y",
      "substitutions": [
        {
          "value": 125.0,
          "unit": "kPa",
          "symbol": "p"
        },
        {
          "value": 70.0,
          "unit": "kN*m",
          "symbol": "Mx_base"
        },
        {
          "value": 2.0,
          "unit": "m3",
          "symbol": "Wx"
        },
        {
          "value": -60.0,
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
        }
      ],
      "result": {
        "value": 70.0,
        "unit": "kPa"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Явные веса: V=N+G_fund+G_soil+G_other; M_base=M+Q*h+M_add_base. Нагрузки конструкции на обрезе, дополнительные моменты на подошве; решение инженера 2026-11-22."
      }
    },
    {
      "kind": "engineer_formula",
      "step_id": "p_corner_mm",
      "expression": "p_{mm}=p+s_x M_{x,base}/W_x+s_y M_{y,base}/W_y",
      "substitutions": [
        {
          "value": 125.0,
          "unit": "kPa",
          "symbol": "p"
        },
        {
          "value": 70.0,
          "unit": "kN*m",
          "symbol": "Mx_base"
        },
        {
          "value": 2.0,
          "unit": "m3",
          "symbol": "Wx"
        },
        {
          "value": -60.0,
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
        }
      ],
      "result": {
        "value": 110.0,
        "unit": "kPa"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Явные веса: V=N+G_fund+G_soil+G_other; M_base=M+Q*h+M_add_base. Нагрузки конструкции на обрезе, дополнительные моменты на подошве; решение инженера 2026-11-22."
      }
    },
    {
      "kind": "engineer_formula",
      "step_id": "p_corner_min",
      "expression": "p_{corner,min}=\\min(p_{++},p_{+-},p_{-+},p_{--})",
      "substitutions": [
        {
          "value": 140.0,
          "unit": "kPa",
          "symbol": "p_corner_pp"
        },
        {
          "value": 180.0,
          "unit": "kPa",
          "symbol": "p_corner_pm"
        },
        {
          "value": 70.0,
          "unit": "kPa",
          "symbol": "p_corner_mp"
        },
        {
          "value": 110.0,
          "unit": "kPa",
          "symbol": "p_corner_mm"
        }
      ],
      "result": {
        "value": 70.0,
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
          "value": 140.0,
          "unit": "kPa",
          "symbol": "p_corner_pp"
        },
        {
          "value": 180.0,
          "unit": "kPa",
          "symbol": "p_corner_pm"
        },
        {
          "value": 70.0,
          "unit": "kPa",
          "symbol": "p_corner_mp"
        },
        {
          "value": 110.0,
          "unit": "kPa",
          "symbol": "p_corner_mm"
        }
      ],
      "result": {
        "value": 180.0,
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
          "value": 125.0,
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
        "value": 125.0,
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
          "value": 160.0,
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
        "value": 160.0,
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
          "value": 145.0,
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
        "value": 145.0,
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
          "value": 180.0,
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
        "value": 180.0,
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
  "unverified_step_count": 20,
  "result_id": "dec00000-0000-4000-8000-000000000003",
  "parameter_source": {
    "kind": "interim",
    "data_sha256": "faaa0724af57ca6c8066f558c4e75c2785d099b34cbfb07c4a85892fdc3b68fe", // pragma: allowlist secret
    "profile": "strict"
  }
} satisfies components['schemas']['ResultEnvelope']
export const weightsBiaxialContext = {
  "status": "available",
  "context": {
    "schema_version": "foundation-result-context-v1",
    "result_id": "dec00000-0000-4000-8000-000000000003",
    "calculation_type": "foundations_shallow_weights",
    "methodology_version": "rectangular-explicit-weights-v1",
    "input_hash": "afd729fb2996b377bb3761eb2e95a21df256a5461a07974cb01d9ba2f4de59a3", // pragma: allowlist secret
    "load_level": "upper_cut",
    "weight_mode": "explicit",
    "inputs": {
      "b": {
        "value": 2.0,
        "unit": "m"
      },
      "d_1": {
        "value": 1.0,
        "unit": "m"
      },
      "d_b": {
        "value": 0.0,
        "unit": "m"
      },
      "gamma_II": {
        "value": 20.0,
        "unit": "kN/m3"
      },
      "gamma_II_prime": {
        "value": 20.0,
        "unit": "kN/m3"
      },
      "c_II": {
        "value": 10.0,
        "unit": "kPa"
      },
      "phi_II": {
        "value": 20.0,
        "unit": "deg"
      },
      "l": {
        "value": 3.0,
        "unit": "m"
      },
      "h": {
        "value": 1.0,
        "unit": "m"
      },
      "N": {
        "value": 600.0,
        "unit": "kN"
      },
      "Mx": {
        "value": 40.0,
        "unit": "kN*m"
      },
      "My": {
        "value": -30.0,
        "unit": "kN*m"
      },
      "Qx": {
        "value": 20.0,
        "unit": "kN"
      },
      "Qy": {
        "value": -15.0,
        "unit": "kN"
      },
      "G_fund": {
        "value": 60.0,
        "unit": "kN"
      },
      "G_soil": {
        "value": 40.0,
        "unit": "kN"
      },
      "G_other": {
        "value": 50.0,
        "unit": "kN"
      },
      "Mx_add_base": {
        "value": 10.0,
        "unit": "kN*m"
      },
      "My_add_base": {
        "value": -15.0,
        "unit": "kN*m"
      }
    },
    "geometry": {
      "b": {
        "value": 2.0,
        "unit": "m"
      },
      "l": {
        "value": 3.0,
        "unit": "m"
      },
      "A": {
        "value": 6.0,
        "unit": "m2"
      },
      "Wx": {
        "value": 2.0,
        "unit": "m3"
      },
      "Wy": {
        "value": 3.0,
        "unit": "m3"
      }
    },
    "trace_values": {
      "gamma_c1": {
        "value": 1.1,
        "unit": "1"
      },
      "gamma_c2": {
        "value": 1.0,
        "unit": "1"
      },
      "k": {
        "value": 1.0,
        "unit": "1"
      },
      "M_gamma": {
        "value": 0.51,
        "unit": "1"
      },
      "M_q": {
        "value": 3.06,
        "unit": "1"
      },
      "M_c": {
        "value": 5.66,
        "unit": "1"
      },
      "k_z": {
        "value": 1.0,
        "unit": "1"
      },
      "R": {
        "value": 152.02,
        "unit": "kPa"
      },
      "A": {
        "value": 6.0,
        "unit": "m2"
      },
      "Wx": {
        "value": 2.0,
        "unit": "m3"
      },
      "Wy": {
        "value": 3.0,
        "unit": "m3"
      },
      "Mx_base": {
        "value": 70.0,
        "unit": "kN*m"
      },
      "My_base": {
        "value": -60.0,
        "unit": "kN*m"
      },
      "G_sum": {
        "value": 150.0,
        "unit": "kN"
      },
      "V": {
        "value": 750.0,
        "unit": "kN"
      },
      "p": {
        "value": 125.0,
        "unit": "kPa"
      },
      "p_x_min": {
        "value": 90.0,
        "unit": "kPa"
      },
      "p_x_max": {
        "value": 160.0,
        "unit": "kPa"
      },
      "e_x": {
        "value": 0.09333333333333334,
        "unit": "m"
      },
      "relative_eccentricity_x": {
        "value": 1.0,
        "unit": "1"
      },
      "pressure_diagram_x": {
        "value": 0.09333333333333334,
        "unit": "m"
      },
      "p_y_min": {
        "value": 105.0,
        "unit": "kPa"
      },
      "p_y_max": {
        "value": 145.0,
        "unit": "kPa"
      },
      "e_y": {
        "value": 0.08,
        "unit": "m"
      },
      "relative_eccentricity_y": {
        "value": 1.0,
        "unit": "1"
      },
      "pressure_diagram_y": {
        "value": 0.08,
        "unit": "m"
      },
      "p_corner_pp": {
        "value": 140.0,
        "unit": "kPa"
      },
      "p_corner_pm": {
        "value": 180.0,
        "unit": "kPa"
      },
      "p_corner_mp": {
        "value": 70.0,
        "unit": "kPa"
      },
      "p_corner_mm": {
        "value": 110.0,
        "unit": "kPa"
      },
      "p_corner_min": {
        "value": 70.0,
        "unit": "kPa"
      },
      "p_corner_max": {
        "value": 180.0,
        "unit": "kPa"
      },
      "edge_limit_multiplier": {
        "value": 1.2,
        "unit": "1"
      },
      "edge_limit": {
        "value": 182.424,
        "unit": "kPa"
      },
      "corner_limit_multiplier": {
        "value": 1.5,
        "unit": "1"
      },
      "corner_limit": {
        "value": 228.03000000000003,
        "unit": "kPa"
      },
      "p_le_R": {
        "value": 125.0,
        "unit": "kPa"
      },
      "p_x_max_le_limit": {
        "value": 160.0,
        "unit": "kPa"
      },
      "p_y_max_le_limit": {
        "value": 145.0,
        "unit": "kPa"
      },
      "p_corner_max_le_limit": {
        "value": 180.0,
        "unit": "kPa"
      }
    },
    "pressure_state": "full_contact",
    "corners": [
      {
        "name": "pp",
        "x": {
          "value": 1.0,
          "unit": "m"
        },
        "y": {
          "value": 1.5,
          "unit": "m"
        },
        "pressure": {
          "value": 140.0,
          "unit": "kPa"
        },
        "step_id": "p_corner_pp"
      },
      {
        "name": "pm",
        "x": {
          "value": 1.0,
          "unit": "m"
        },
        "y": {
          "value": -1.5,
          "unit": "m"
        },
        "pressure": {
          "value": 180.0,
          "unit": "kPa"
        },
        "step_id": "p_corner_pm"
      },
      {
        "name": "mp",
        "x": {
          "value": -1.0,
          "unit": "m"
        },
        "y": {
          "value": 1.5,
          "unit": "m"
        },
        "pressure": {
          "value": 70.0,
          "unit": "kPa"
        },
        "step_id": "p_corner_mp"
      },
      {
        "name": "mm",
        "x": {
          "value": -1.0,
          "unit": "m"
        },
        "y": {
          "value": -1.5,
          "unit": "m"
        },
        "pressure": {
          "value": 110.0,
          "unit": "kPa"
        },
        "step_id": "p_corner_mm"
      }
    ]
  }
} satisfies components['schemas']['FoundationContextResponse']
export const weightsContactRefusalRequest = {
  "calculation_type": "foundations_shallow_weights",
  "inputs": {
    "b": {
      "value": 2.0,
      "unit": "m"
    },
    "d_1": {
      "value": 1.0,
      "unit": "m"
    },
    "d_b": {
      "value": 0.0,
      "unit": "m"
    },
    "gamma_II": {
      "value": 20.0,
      "unit": "kN/m3"
    },
    "gamma_II_prime": {
      "value": 20.0,
      "unit": "kN/m3"
    },
    "c_II": {
      "value": 10.0,
      "unit": "kPa"
    },
    "phi_II": {
      "value": 20.0,
      "unit": "deg"
    },
    "l": {
      "value": 3.0,
      "unit": "m"
    },
    "h": {
      "value": 1.0,
      "unit": "m"
    },
    "N": {
      "value": 600.0,
      "unit": "kN"
    },
    "Mx": {
      "value": 40.0,
      "unit": "kN*m"
    },
    "My": {
      "value": -30.0,
      "unit": "kN*m"
    },
    "Qx": {
      "value": 20.0,
      "unit": "kN"
    },
    "Qy": {
      "value": -15.0,
      "unit": "kN"
    },
    "G_fund": {
      "value": 60.0,
      "unit": "kN"
    },
    "G_soil": {
      "value": 40.0,
      "unit": "kN"
    },
    "G_other": {
      "value": 50.0,
      "unit": "kN"
    },
    "Mx_add_base": {
      "value": 2000.0,
      "unit": "kN*m"
    },
    "My_add_base": {
      "value": -15.0,
      "unit": "kN*m"
    }
  }
} satisfies components['schemas']['CalculationRequest']
export const weightsContactRefusalEnvelope = {
  "engine_version": "0.1.0",
  "input_hash": "8e8a61f47323c457fa7bf4532ee25a259ecf065c243c6133d534618b4316c265", // pragma: allowlist secret
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
    }
  ],
  "engineer_rules": [
    {
      "engineer": "Аким",
      "rationale": "Геометрия прямоугольной подошвы: A=b*l, Wx=l*b²/6, Wy=b*l²/6; инженерный контракт 2026-11-08."
    },
    {
      "engineer": "Аким",
      "rationale": "Явные веса: V=N+G_fund+G_soil+G_other; M_base=M+Q*h+M_add_base. Нагрузки конструкции на обрезе, дополнительные моменты на подошве; решение инженера 2026-11-22."
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
      "value": -925.0,
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
      "G_fund",
      "G_soil",
      "G_other",
      "Mx_add_base",
      "My_add_base"
    ],
    "limiting_corner": "mp"
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
      "expression": "M_{x,base}=M_x+Q_x h+M_{x,add,base}",
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
        },
        {
          "value": 2000.0,
          "unit": "kN*m",
          "symbol": "Mx_add_base"
        }
      ],
      "result": {
        "value": 2060.0,
        "unit": "kN*m"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Явные веса: V=N+G_fund+G_soil+G_other; M_base=M+Q*h+M_add_base. Нагрузки конструкции на обрезе, дополнительные моменты на подошве; решение инженера 2026-11-22."
      }
    },
    {
      "kind": "engineer_formula",
      "step_id": "My_base",
      "expression": "M_{y,base}=M_y+Q_y h+M_{y,add,base}",
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
        },
        {
          "value": -15.0,
          "unit": "kN*m",
          "symbol": "My_add_base"
        }
      ],
      "result": {
        "value": -60.0,
        "unit": "kN*m"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Явные веса: V=N+G_fund+G_soil+G_other; M_base=M+Q*h+M_add_base. Нагрузки конструкции на обрезе, дополнительные моменты на подошве; решение инженера 2026-11-22."
      }
    },
    {
      "kind": "engineer_formula",
      "step_id": "G_sum",
      "expression": "G_{sum}=G_{fund}+G_{soil}+G_{other}",
      "substitutions": [
        {
          "value": 60.0,
          "unit": "kN",
          "symbol": "G_fund"
        },
        {
          "value": 40.0,
          "unit": "kN",
          "symbol": "G_soil"
        },
        {
          "value": 50.0,
          "unit": "kN",
          "symbol": "G_other"
        }
      ],
      "result": {
        "value": 150.0,
        "unit": "kN"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Явные веса: V=N+G_fund+G_soil+G_other; M_base=M+Q*h+M_add_base. Нагрузки конструкции на обрезе, дополнительные моменты на подошве; решение инженера 2026-11-22."
      }
    },
    {
      "kind": "engineer_formula",
      "step_id": "V",
      "expression": "V=N+G_{sum}",
      "substitutions": [
        {
          "value": 600.0,
          "unit": "kN",
          "symbol": "N"
        },
        {
          "value": 150.0,
          "unit": "kN",
          "symbol": "G_sum"
        }
      ],
      "result": {
        "value": 750.0,
        "unit": "kN"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Явные веса: V=N+G_fund+G_soil+G_other; M_base=M+Q*h+M_add_base. Нагрузки конструкции на обрезе, дополнительные моменты на подошве; решение инженера 2026-11-22."
      }
    },
    {
      "kind": "engineer_formula",
      "step_id": "p",
      "expression": "p=V/A",
      "substitutions": [
        {
          "value": 750.0,
          "unit": "kN",
          "symbol": "V"
        },
        {
          "value": 6.0,
          "unit": "m2",
          "symbol": "A"
        }
      ],
      "result": {
        "value": 125.0,
        "unit": "kPa"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Явные веса: V=N+G_fund+G_soil+G_other; M_base=M+Q*h+M_add_base. Нагрузки конструкции на обрезе, дополнительные моменты на подошве; решение инженера 2026-11-22."
      }
    },
    {
      "kind": "engineer_formula",
      "step_id": "p_x_min",
      "expression": "p_{x,min}=p-|M_{x,base}|/W_x",
      "substitutions": [
        {
          "value": 125.0,
          "unit": "kPa",
          "symbol": "p"
        },
        {
          "value": 2060.0,
          "unit": "kN*m",
          "symbol": "Mx_base"
        },
        {
          "value": 2.0,
          "unit": "m3",
          "symbol": "Wx"
        }
      ],
      "result": {
        "value": -905.0,
        "unit": "kPa"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Явные веса: V=N+G_fund+G_soil+G_other; M_base=M+Q*h+M_add_base. Нагрузки конструкции на обрезе, дополнительные моменты на подошве; решение инженера 2026-11-22."
      }
    },
    {
      "kind": "engineer_formula",
      "step_id": "p_x_max",
      "expression": "p_{x,max}=p+|M_{x,base}|/W_x",
      "substitutions": [
        {
          "value": 125.0,
          "unit": "kPa",
          "symbol": "p"
        },
        {
          "value": 2060.0,
          "unit": "kN*m",
          "symbol": "Mx_base"
        },
        {
          "value": 2.0,
          "unit": "m3",
          "symbol": "Wx"
        }
      ],
      "result": {
        "value": 1155.0,
        "unit": "kPa"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Явные веса: V=N+G_fund+G_soil+G_other; M_base=M+Q*h+M_add_base. Нагрузки конструкции на обрезе, дополнительные моменты на подошве; решение инженера 2026-11-22."
      }
    },
    {
      "kind": "engineer_formula",
      "step_id": "e_x",
      "expression": "e_x=|M_{x,base}|/V",
      "substitutions": [
        {
          "value": 2060.0,
          "unit": "kN*m",
          "symbol": "Mx_base"
        },
        {
          "value": 750.0,
          "unit": "kN",
          "symbol": "V"
        }
      ],
      "result": {
        "value": 2.7466666666666666,
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
          "value": 1.3733333333333333,
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
        "value": 0.0,
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
      "kind": "engineer_formula",
      "step_id": "p_y_min",
      "expression": "p_{y,min}=p-|M_{y,base}|/W_y",
      "substitutions": [
        {
          "value": 125.0,
          "unit": "kPa",
          "symbol": "p"
        },
        {
          "value": -60.0,
          "unit": "kN*m",
          "symbol": "My_base"
        },
        {
          "value": 3.0,
          "unit": "m3",
          "symbol": "Wy"
        }
      ],
      "result": {
        "value": 105.0,
        "unit": "kPa"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Явные веса: V=N+G_fund+G_soil+G_other; M_base=M+Q*h+M_add_base. Нагрузки конструкции на обрезе, дополнительные моменты на подошве; решение инженера 2026-11-22."
      }
    },
    {
      "kind": "engineer_formula",
      "step_id": "p_y_max",
      "expression": "p_{y,max}=p+|M_{y,base}|/W_y",
      "substitutions": [
        {
          "value": 125.0,
          "unit": "kPa",
          "symbol": "p"
        },
        {
          "value": -60.0,
          "unit": "kN*m",
          "symbol": "My_base"
        },
        {
          "value": 3.0,
          "unit": "m3",
          "symbol": "Wy"
        }
      ],
      "result": {
        "value": 145.0,
        "unit": "kPa"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Явные веса: V=N+G_fund+G_soil+G_other; M_base=M+Q*h+M_add_base. Нагрузки конструкции на обрезе, дополнительные моменты на подошве; решение инженера 2026-11-22."
      }
    },
    {
      "kind": "engineer_formula",
      "step_id": "e_y",
      "expression": "e_y=|M_{y,base}|/V",
      "substitutions": [
        {
          "value": -60.0,
          "unit": "kN*m",
          "symbol": "My_base"
        },
        {
          "value": 750.0,
          "unit": "kN",
          "symbol": "V"
        }
      ],
      "result": {
        "value": 0.08,
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
          "value": 0.02666666666666667,
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
          "value": 0.08,
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
        "value": 0.08,
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
      "kind": "engineer_formula",
      "step_id": "p_corner_pp",
      "expression": "p_{pp}=p+s_x M_{x,base}/W_x+s_y M_{y,base}/W_y",
      "substitutions": [
        {
          "value": 125.0,
          "unit": "kPa",
          "symbol": "p"
        },
        {
          "value": 2060.0,
          "unit": "kN*m",
          "symbol": "Mx_base"
        },
        {
          "value": 2.0,
          "unit": "m3",
          "symbol": "Wx"
        },
        {
          "value": -60.0,
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
        }
      ],
      "result": {
        "value": 1135.0,
        "unit": "kPa"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Явные веса: V=N+G_fund+G_soil+G_other; M_base=M+Q*h+M_add_base. Нагрузки конструкции на обрезе, дополнительные моменты на подошве; решение инженера 2026-11-22."
      }
    },
    {
      "kind": "engineer_formula",
      "step_id": "p_corner_pm",
      "expression": "p_{pm}=p+s_x M_{x,base}/W_x+s_y M_{y,base}/W_y",
      "substitutions": [
        {
          "value": 125.0,
          "unit": "kPa",
          "symbol": "p"
        },
        {
          "value": 2060.0,
          "unit": "kN*m",
          "symbol": "Mx_base"
        },
        {
          "value": 2.0,
          "unit": "m3",
          "symbol": "Wx"
        },
        {
          "value": -60.0,
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
        }
      ],
      "result": {
        "value": 1175.0,
        "unit": "kPa"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Явные веса: V=N+G_fund+G_soil+G_other; M_base=M+Q*h+M_add_base. Нагрузки конструкции на обрезе, дополнительные моменты на подошве; решение инженера 2026-11-22."
      }
    },
    {
      "kind": "engineer_formula",
      "step_id": "p_corner_mp",
      "expression": "p_{mp}=p+s_x M_{x,base}/W_x+s_y M_{y,base}/W_y",
      "substitutions": [
        {
          "value": 125.0,
          "unit": "kPa",
          "symbol": "p"
        },
        {
          "value": 2060.0,
          "unit": "kN*m",
          "symbol": "Mx_base"
        },
        {
          "value": 2.0,
          "unit": "m3",
          "symbol": "Wx"
        },
        {
          "value": -60.0,
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
        }
      ],
      "result": {
        "value": -925.0,
        "unit": "kPa"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Явные веса: V=N+G_fund+G_soil+G_other; M_base=M+Q*h+M_add_base. Нагрузки конструкции на обрезе, дополнительные моменты на подошве; решение инженера 2026-11-22."
      }
    },
    {
      "kind": "engineer_formula",
      "step_id": "p_corner_mm",
      "expression": "p_{mm}=p+s_x M_{x,base}/W_x+s_y M_{y,base}/W_y",
      "substitutions": [
        {
          "value": 125.0,
          "unit": "kPa",
          "symbol": "p"
        },
        {
          "value": 2060.0,
          "unit": "kN*m",
          "symbol": "Mx_base"
        },
        {
          "value": 2.0,
          "unit": "m3",
          "symbol": "Wx"
        },
        {
          "value": -60.0,
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
        }
      ],
      "result": {
        "value": -885.0,
        "unit": "kPa"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Явные веса: V=N+G_fund+G_soil+G_other; M_base=M+Q*h+M_add_base. Нагрузки конструкции на обрезе, дополнительные моменты на подошве; решение инженера 2026-11-22."
      }
    },
    {
      "kind": "engineer_formula",
      "step_id": "p_corner_min",
      "expression": "p_{corner,min}=\\min(p_{++},p_{+-},p_{-+},p_{--})",
      "substitutions": [
        {
          "value": 1135.0,
          "unit": "kPa",
          "symbol": "p_corner_pp"
        },
        {
          "value": 1175.0,
          "unit": "kPa",
          "symbol": "p_corner_pm"
        },
        {
          "value": -925.0,
          "unit": "kPa",
          "symbol": "p_corner_mp"
        },
        {
          "value": -885.0,
          "unit": "kPa",
          "symbol": "p_corner_mm"
        }
      ],
      "result": {
        "value": -925.0,
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
          "value": 1135.0,
          "unit": "kPa",
          "symbol": "p_corner_pp"
        },
        {
          "value": 1175.0,
          "unit": "kPa",
          "symbol": "p_corner_pm"
        },
        {
          "value": -925.0,
          "unit": "kPa",
          "symbol": "p_corner_mp"
        },
        {
          "value": -885.0,
          "unit": "kPa",
          "symbol": "p_corner_mm"
        }
      ],
      "result": {
        "value": 1175.0,
        "unit": "kPa"
      },
      "source": {
        "engineer": "Аким",
        "rationale": "Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08."
      }
    }
  ],
  "unverified_step_count": 11,
  "result_id": "dec00000-0000-4000-8000-000000000004",
  "parameter_source": {
    "kind": "interim",
    "data_sha256": "faaa0724af57ca6c8066f558c4e75c2785d099b34cbfb07c4a85892fdc3b68fe", // pragma: allowlist secret
    "profile": "strict"
  }
} satisfies components['schemas']['ResultEnvelope']
export const weightsContactRefusalContext = {
  "status": "available",
  "context": {
    "schema_version": "foundation-result-context-v1",
    "result_id": "dec00000-0000-4000-8000-000000000004",
    "calculation_type": "foundations_shallow_weights",
    "methodology_version": "rectangular-explicit-weights-v1",
    "input_hash": "8e8a61f47323c457fa7bf4532ee25a259ecf065c243c6133d534618b4316c265", // pragma: allowlist secret
    "load_level": "upper_cut",
    "weight_mode": "explicit",
    "inputs": {
      "b": {
        "value": 2.0,
        "unit": "m"
      },
      "d_1": {
        "value": 1.0,
        "unit": "m"
      },
      "d_b": {
        "value": 0.0,
        "unit": "m"
      },
      "gamma_II": {
        "value": 20.0,
        "unit": "kN/m3"
      },
      "gamma_II_prime": {
        "value": 20.0,
        "unit": "kN/m3"
      },
      "c_II": {
        "value": 10.0,
        "unit": "kPa"
      },
      "phi_II": {
        "value": 20.0,
        "unit": "deg"
      },
      "l": {
        "value": 3.0,
        "unit": "m"
      },
      "h": {
        "value": 1.0,
        "unit": "m"
      },
      "N": {
        "value": 600.0,
        "unit": "kN"
      },
      "Mx": {
        "value": 40.0,
        "unit": "kN*m"
      },
      "My": {
        "value": -30.0,
        "unit": "kN*m"
      },
      "Qx": {
        "value": 20.0,
        "unit": "kN"
      },
      "Qy": {
        "value": -15.0,
        "unit": "kN"
      },
      "G_fund": {
        "value": 60.0,
        "unit": "kN"
      },
      "G_soil": {
        "value": 40.0,
        "unit": "kN"
      },
      "G_other": {
        "value": 50.0,
        "unit": "kN"
      },
      "Mx_add_base": {
        "value": 2000.0,
        "unit": "kN*m"
      },
      "My_add_base": {
        "value": -15.0,
        "unit": "kN*m"
      }
    },
    "geometry": {
      "b": {
        "value": 2.0,
        "unit": "m"
      },
      "l": {
        "value": 3.0,
        "unit": "m"
      },
      "A": {
        "value": 6.0,
        "unit": "m2"
      },
      "Wx": {
        "value": 2.0,
        "unit": "m3"
      },
      "Wy": {
        "value": 3.0,
        "unit": "m3"
      }
    },
    "trace_values": {
      "gamma_c1": {
        "value": 1.1,
        "unit": "1"
      },
      "gamma_c2": {
        "value": 1.0,
        "unit": "1"
      },
      "k": {
        "value": 1.0,
        "unit": "1"
      },
      "M_gamma": {
        "value": 0.51,
        "unit": "1"
      },
      "M_q": {
        "value": 3.06,
        "unit": "1"
      },
      "M_c": {
        "value": 5.66,
        "unit": "1"
      },
      "k_z": {
        "value": 1.0,
        "unit": "1"
      },
      "R": {
        "value": 152.02,
        "unit": "kPa"
      },
      "A": {
        "value": 6.0,
        "unit": "m2"
      },
      "Wx": {
        "value": 2.0,
        "unit": "m3"
      },
      "Wy": {
        "value": 3.0,
        "unit": "m3"
      },
      "Mx_base": {
        "value": 2060.0,
        "unit": "kN*m"
      },
      "My_base": {
        "value": -60.0,
        "unit": "kN*m"
      },
      "G_sum": {
        "value": 150.0,
        "unit": "kN"
      },
      "V": {
        "value": 750.0,
        "unit": "kN"
      },
      "p": {
        "value": 125.0,
        "unit": "kPa"
      },
      "p_x_min": {
        "value": -905.0,
        "unit": "kPa"
      },
      "p_x_max": {
        "value": 1155.0,
        "unit": "kPa"
      },
      "e_x": {
        "value": 2.7466666666666666,
        "unit": "m"
      },
      "relative_eccentricity_x": {
        "value": 0.0,
        "unit": "1"
      },
      "p_y_min": {
        "value": 105.0,
        "unit": "kPa"
      },
      "p_y_max": {
        "value": 145.0,
        "unit": "kPa"
      },
      "e_y": {
        "value": 0.08,
        "unit": "m"
      },
      "relative_eccentricity_y": {
        "value": 1.0,
        "unit": "1"
      },
      "pressure_diagram_y": {
        "value": 0.08,
        "unit": "m"
      },
      "p_corner_pp": {
        "value": 1135.0,
        "unit": "kPa"
      },
      "p_corner_pm": {
        "value": 1175.0,
        "unit": "kPa"
      },
      "p_corner_mp": {
        "value": -925.0,
        "unit": "kPa"
      },
      "p_corner_mm": {
        "value": -885.0,
        "unit": "kPa"
      },
      "p_corner_min": {
        "value": -925.0,
        "unit": "kPa"
      },
      "p_corner_max": {
        "value": 1175.0,
        "unit": "kPa"
      }
    },
    "pressure_state": "diagnostic",
    "corners": [
      {
        "name": "pp",
        "x": {
          "value": 1.0,
          "unit": "m"
        },
        "y": {
          "value": 1.5,
          "unit": "m"
        },
        "pressure": {
          "value": 1135.0,
          "unit": "kPa"
        },
        "step_id": "p_corner_pp"
      },
      {
        "name": "pm",
        "x": {
          "value": 1.0,
          "unit": "m"
        },
        "y": {
          "value": -1.5,
          "unit": "m"
        },
        "pressure": {
          "value": 1175.0,
          "unit": "kPa"
        },
        "step_id": "p_corner_pm"
      },
      {
        "name": "mp",
        "x": {
          "value": -1.0,
          "unit": "m"
        },
        "y": {
          "value": 1.5,
          "unit": "m"
        },
        "pressure": {
          "value": -925.0,
          "unit": "kPa"
        },
        "step_id": "p_corner_mp"
      },
      {
        "name": "mm",
        "x": {
          "value": -1.0,
          "unit": "m"
        },
        "y": {
          "value": -1.5,
          "unit": "m"
        },
        "pressure": {
          "value": -885.0,
          "unit": "kPa"
        },
        "step_id": "p_corner_mm"
      }
    ]
  }
} satisfies components['schemas']['FoundationContextResponse']
export const selectionSelected = {
  "schema_version": "foundation-selection-result-v1",
  "selection_id": "dec00000-0000-4000-8000-000000000007",
  "input_hash": "6e61a000d66b23f9e3890a0b27641ddc029a883fa65484db623e23b23ed33fb7", // pragma: allowlist secret
  "request": {
    "schema_version": "foundation-selection-request-v1",
    "calculation_type": "foundations_shallow_loads",
    "policy_version": "foundation-min-area-v1",
    "common_inputs": {
      "d_1": {
        "value": 1.0,
        "unit": "m"
      },
      "d_b": {
        "value": 0.0,
        "unit": "m"
      },
      "gamma_II": {
        "value": 20.0,
        "unit": "kN/m3"
      },
      "gamma_II_prime": {
        "value": 20.0,
        "unit": "kN/m3"
      },
      "c_II": {
        "value": 10.0,
        "unit": "kPa"
      },
      "phi_II": {
        "value": 20.0,
        "unit": "deg"
      },
      "h": {
        "value": 1.0,
        "unit": "m"
      },
      "d": {
        "value": 1.0,
        "unit": "m"
      },
      "N": {
        "value": 600.0,
        "unit": "kN"
      },
      "Mx": {
        "value": 0.0,
        "unit": "kN*m"
      },
      "My": {
        "value": 0.0,
        "unit": "kN*m"
      },
      "Qx": {
        "value": 0.0,
        "unit": "kN"
      },
      "Qy": {
        "value": 0.0,
        "unit": "kN"
      }
    },
    "candidates": [
      {
        "b": {
          "value": 2.0,
          "unit": "m"
        },
        "l": {
          "value": 2.0,
          "unit": "m"
        }
      },
      {
        "b": {
          "value": 2.0,
          "unit": "m"
        },
        "l": {
          "value": 3.0,
          "unit": "m"
        }
      }
    ]
  },
  "status": "selected",
  "outcomes": [
    {
      "index": 0,
      "candidate": {
        "b": {
          "value": 2.0,
          "unit": "m"
        },
        "l": {
          "value": 2.0,
          "unit": "m"
        }
      },
      "status": "evaluated",
      "envelope": {
        "engine_version": "0.1.0",
        "input_hash": "1702117dd078e7f853f9ef66707546138d81133890ca676ea11caf5ad6c457d9", // pragma: allowlist secret
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
                "value": 2.0,
                "unit": "m",
                "symbol": "l"
              }
            ],
            "result": {
              "value": 4.0,
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
                "value": 2.0,
                "unit": "m",
                "symbol": "l"
              }
            ],
            "result": {
              "value": 1.3333333333333333,
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
                "value": 2.0,
                "unit": "m",
                "symbol": "l"
              }
            ],
            "result": {
              "value": 1.3333333333333333,
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
                "value": 4.0,
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
                "value": 1.3333333333333333,
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
                "value": 4.0,
                "unit": "m2",
                "symbol": "A"
              }
            ],
            "result": {
              "value": 680.0,
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
                "value": 4.0,
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
                "value": 1.3333333333333333,
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
                "value": 600.0,
                "unit": "kN",
                "symbol": "N"
              },
              {
                "value": 4.0,
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
                "value": 1.3333333333333333,
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
                "value": 680.0,
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
                "value": 4.0,
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
                "value": 1.3333333333333333,
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
                "value": 600.0,
                "unit": "kN",
                "symbol": "N"
              },
              {
                "value": 4.0,
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
                "value": 1.3333333333333333,
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
                "value": 680.0,
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
            "step_id": "corner_component_pp",
            "expression": "P_{\\max}=\\frac{N}{A}+\\gamma_{mt}d+\\frac{M_x}{W_x}+\\frac{M_y}{W_y}",
            "substitutions": [
              {
                "value": 600.0,
                "unit": "kN",
                "symbol": "N"
              },
              {
                "value": 4.0,
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
                "value": 1.3333333333333333,
                "unit": "m3",
                "symbol": "W_x"
              },
              {
                "value": 0.0,
                "unit": "kN*m",
                "symbol": "M_y"
              },
              {
                "value": 1.3333333333333333,
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
                "value": 1.3333333333333333,
                "unit": "m3",
                "symbol": "Wx"
              },
              {
                "value": 0.0,
                "unit": "kN*m",
                "symbol": "My_base"
              },
              {
                "value": 1.3333333333333333,
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
                "value": 600.0,
                "unit": "kN",
                "symbol": "N"
              },
              {
                "value": 4.0,
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
                "value": 1.3333333333333333,
                "unit": "m3",
                "symbol": "W_x"
              },
              {
                "value": -0.0,
                "unit": "kN*m",
                "symbol": "M_y"
              },
              {
                "value": 1.3333333333333333,
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
                "value": 1.3333333333333333,
                "unit": "m3",
                "symbol": "Wx"
              },
              {
                "value": 0.0,
                "unit": "kN*m",
                "symbol": "My_base"
              },
              {
                "value": 1.3333333333333333,
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
                "value": 600.0,
                "unit": "kN",
                "symbol": "N"
              },
              {
                "value": 4.0,
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
                "value": 1.3333333333333333,
                "unit": "m3",
                "symbol": "W_x"
              },
              {
                "value": 0.0,
                "unit": "kN*m",
                "symbol": "M_y"
              },
              {
                "value": 1.3333333333333333,
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
                "value": 1.3333333333333333,
                "unit": "m3",
                "symbol": "Wx"
              },
              {
                "value": 0.0,
                "unit": "kN*m",
                "symbol": "My_base"
              },
              {
                "value": 1.3333333333333333,
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
                "value": 600.0,
                "unit": "kN",
                "symbol": "N"
              },
              {
                "value": 4.0,
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
                "value": 1.3333333333333333,
                "unit": "m3",
                "symbol": "W_x"
              },
              {
                "value": -0.0,
                "unit": "kN*m",
                "symbol": "M_y"
              },
              {
                "value": 1.3333333333333333,
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
                "value": 1.3333333333333333,
                "unit": "m3",
                "symbol": "Wx"
              },
              {
                "value": 0.0,
                "unit": "kN*m",
                "symbol": "My_base"
              },
              {
                "value": 1.3333333333333333,
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
        "result_id": "dec00000-0000-4000-8000-000000000005",
        "parameter_source": {
          "kind": "interim",
          "data_sha256": "faaa0724af57ca6c8066f558c4e75c2785d099b34cbfb07c4a85892fdc3b68fe", // pragma: allowlist secret
          "profile": "strict"
        }
      },
      "reason": null
    },
    {
      "index": 1,
      "candidate": {
        "b": {
          "value": 2.0,
          "unit": "m"
        },
        "l": {
          "value": 3.0,
          "unit": "m"
        }
      },
      "status": "evaluated",
      "envelope": {
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
        "result_id": "dec00000-0000-4000-8000-000000000006",
        "parameter_source": {
          "kind": "interim",
          "data_sha256": "faaa0724af57ca6c8066f558c4e75c2785d099b34cbfb07c4a85892fdc3b68fe", // pragma: allowlist secret
          "profile": "strict"
        }
      },
      "reason": null
    }
  ],
  "stop_reason": null,
  "selected_candidate_index": 1,
  "selected_result_id": "dec00000-0000-4000-8000-000000000006"
} satisfies components['schemas']['FoundationSelectionResult']
export const selectionWinnerContext = {
  "status": "available",
  "context": {
    "schema_version": "foundation-result-context-v1",
    "result_id": "dec00000-0000-4000-8000-000000000006",
    "calculation_type": "foundations_shallow_loads",
    "methodology_version": "rectangular-full-contact-v1",
    "input_hash": "22c0d8c6334ed14ddcc4f326eda3c8c7f7fc740a1c4890f4fb269ad45be4a552", // pragma: allowlist secret
    "load_level": "upper_cut",
    "weight_mode": "averaged",
    "inputs": {
      "d_1": {
        "value": 1.0,
        "unit": "m"
      },
      "d_b": {
        "value": 0.0,
        "unit": "m"
      },
      "gamma_II": {
        "value": 20.0,
        "unit": "kN/m3"
      },
      "gamma_II_prime": {
        "value": 20.0,
        "unit": "kN/m3"
      },
      "c_II": {
        "value": 10.0,
        "unit": "kPa"
      },
      "phi_II": {
        "value": 20.0,
        "unit": "deg"
      },
      "h": {
        "value": 1.0,
        "unit": "m"
      },
      "d": {
        "value": 1.0,
        "unit": "m"
      },
      "N": {
        "value": 600.0,
        "unit": "kN"
      },
      "Mx": {
        "value": 0.0,
        "unit": "kN*m"
      },
      "My": {
        "value": 0.0,
        "unit": "kN*m"
      },
      "Qx": {
        "value": 0.0,
        "unit": "kN"
      },
      "Qy": {
        "value": 0.0,
        "unit": "kN"
      },
      "b": {
        "value": 2.0,
        "unit": "m"
      },
      "l": {
        "value": 3.0,
        "unit": "m"
      }
    },
    "geometry": {
      "b": {
        "value": 2.0,
        "unit": "m"
      },
      "l": {
        "value": 3.0,
        "unit": "m"
      },
      "A": {
        "value": 6.0,
        "unit": "m2"
      },
      "Wx": {
        "value": 2.0,
        "unit": "m3"
      },
      "Wy": {
        "value": 3.0,
        "unit": "m3"
      }
    },
    "trace_values": {
      "gamma_c1": {
        "value": 1.1,
        "unit": "1"
      },
      "gamma_c2": {
        "value": 1.0,
        "unit": "1"
      },
      "k": {
        "value": 1.0,
        "unit": "1"
      },
      "M_gamma": {
        "value": 0.51,
        "unit": "1"
      },
      "M_q": {
        "value": 3.06,
        "unit": "1"
      },
      "M_c": {
        "value": 5.66,
        "unit": "1"
      },
      "k_z": {
        "value": 1.0,
        "unit": "1"
      },
      "R": {
        "value": 152.02,
        "unit": "kPa"
      },
      "A": {
        "value": 6.0,
        "unit": "m2"
      },
      "Wx": {
        "value": 2.0,
        "unit": "m3"
      },
      "Wy": {
        "value": 3.0,
        "unit": "m3"
      },
      "Mx_base": {
        "value": 0.0,
        "unit": "kN*m"
      },
      "My_base": {
        "value": 0.0,
        "unit": "kN*m"
      },
      "gamma_mt": {
        "value": 20.0,
        "unit": "kN/m3"
      },
      "p": {
        "value": 120.0,
        "unit": "kPa"
      },
      "V": {
        "value": 720.0,
        "unit": "kN"
      },
      "p_x_min": {
        "value": 120.0,
        "unit": "kPa"
      },
      "p_x_max": {
        "value": 120.0,
        "unit": "kPa"
      },
      "e_x": {
        "value": 0.0,
        "unit": "m"
      },
      "relative_eccentricity_x": {
        "value": 1.0,
        "unit": "1"
      },
      "pressure_diagram_x": {
        "value": 0.0,
        "unit": "m"
      },
      "p_y_min": {
        "value": 120.0,
        "unit": "kPa"
      },
      "p_y_max": {
        "value": 120.0,
        "unit": "kPa"
      },
      "e_y": {
        "value": 0.0,
        "unit": "m"
      },
      "relative_eccentricity_y": {
        "value": 1.0,
        "unit": "1"
      },
      "pressure_diagram_y": {
        "value": 0.0,
        "unit": "m"
      },
      "corner_component_pp": {
        "value": 120.0,
        "unit": "kPa"
      },
      "p_corner_pp": {
        "value": 120.0,
        "unit": "kPa"
      },
      "corner_component_pm": {
        "value": 120.0,
        "unit": "kPa"
      },
      "p_corner_pm": {
        "value": 120.0,
        "unit": "kPa"
      },
      "corner_component_mp": {
        "value": 120.0,
        "unit": "kPa"
      },
      "p_corner_mp": {
        "value": 120.0,
        "unit": "kPa"
      },
      "corner_component_mm": {
        "value": 120.0,
        "unit": "kPa"
      },
      "p_corner_mm": {
        "value": 120.0,
        "unit": "kPa"
      },
      "p_corner_min": {
        "value": 120.0,
        "unit": "kPa"
      },
      "p_corner_max": {
        "value": 120.0,
        "unit": "kPa"
      },
      "edge_limit_multiplier": {
        "value": 1.2,
        "unit": "1"
      },
      "edge_limit": {
        "value": 182.424,
        "unit": "kPa"
      },
      "corner_limit_multiplier": {
        "value": 1.5,
        "unit": "1"
      },
      "corner_limit": {
        "value": 228.03000000000003,
        "unit": "kPa"
      },
      "p_le_R": {
        "value": 120.0,
        "unit": "kPa"
      },
      "p_x_max_le_limit": {
        "value": 120.0,
        "unit": "kPa"
      },
      "p_y_max_le_limit": {
        "value": 120.0,
        "unit": "kPa"
      },
      "p_corner_max_le_limit": {
        "value": 120.0,
        "unit": "kPa"
      }
    },
    "pressure_state": "full_contact",
    "corners": [
      {
        "name": "pp",
        "x": {
          "value": 1.0,
          "unit": "m"
        },
        "y": {
          "value": 1.5,
          "unit": "m"
        },
        "pressure": {
          "value": 120.0,
          "unit": "kPa"
        },
        "step_id": "p_corner_pp"
      },
      {
        "name": "pm",
        "x": {
          "value": 1.0,
          "unit": "m"
        },
        "y": {
          "value": -1.5,
          "unit": "m"
        },
        "pressure": {
          "value": 120.0,
          "unit": "kPa"
        },
        "step_id": "p_corner_pm"
      },
      {
        "name": "mp",
        "x": {
          "value": -1.0,
          "unit": "m"
        },
        "y": {
          "value": 1.5,
          "unit": "m"
        },
        "pressure": {
          "value": 120.0,
          "unit": "kPa"
        },
        "step_id": "p_corner_mp"
      },
      {
        "name": "mm",
        "x": {
          "value": -1.0,
          "unit": "m"
        },
        "y": {
          "value": -1.5,
          "unit": "m"
        },
        "pressure": {
          "value": 120.0,
          "unit": "kPa"
        },
        "step_id": "p_corner_mm"
      }
    ]
  }
} satisfies components['schemas']['FoundationContextResponse']
export const selectionExhausted = {
  "schema_version": "foundation-selection-result-v1",
  "selection_id": "dec00000-0000-4000-8000-000000000009",
  "input_hash": "9b25481f1c1557a426cd195145e2a406e9236425143d87457abb84011f2c6e37", // pragma: allowlist secret
  "request": {
    "schema_version": "foundation-selection-request-v1",
    "calculation_type": "foundations_shallow_loads",
    "policy_version": "foundation-min-area-v1",
    "common_inputs": {
      "d_1": {
        "value": 1.0,
        "unit": "m"
      },
      "d_b": {
        "value": 0.0,
        "unit": "m"
      },
      "gamma_II": {
        "value": 20.0,
        "unit": "kN/m3"
      },
      "gamma_II_prime": {
        "value": 20.0,
        "unit": "kN/m3"
      },
      "c_II": {
        "value": 10.0,
        "unit": "kPa"
      },
      "phi_II": {
        "value": 20.0,
        "unit": "deg"
      },
      "h": {
        "value": 1.0,
        "unit": "m"
      },
      "d": {
        "value": 1.0,
        "unit": "m"
      },
      "N": {
        "value": 600.0,
        "unit": "kN"
      },
      "Mx": {
        "value": 0.0,
        "unit": "kN*m"
      },
      "My": {
        "value": 0.0,
        "unit": "kN*m"
      },
      "Qx": {
        "value": 0.0,
        "unit": "kN"
      },
      "Qy": {
        "value": 0.0,
        "unit": "kN"
      }
    },
    "candidates": [
      {
        "b": {
          "value": 2.0,
          "unit": "m"
        },
        "l": {
          "value": 2.0,
          "unit": "m"
        }
      }
    ]
  },
  "status": "no_acceptable_candidate",
  "outcomes": [
    {
      "index": 0,
      "candidate": {
        "b": {
          "value": 2.0,
          "unit": "m"
        },
        "l": {
          "value": 2.0,
          "unit": "m"
        }
      },
      "status": "evaluated",
      "envelope": {
        "engine_version": "0.1.0",
        "input_hash": "1702117dd078e7f853f9ef66707546138d81133890ca676ea11caf5ad6c457d9", // pragma: allowlist secret
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
                "value": 2.0,
                "unit": "m",
                "symbol": "l"
              }
            ],
            "result": {
              "value": 4.0,
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
                "value": 2.0,
                "unit": "m",
                "symbol": "l"
              }
            ],
            "result": {
              "value": 1.3333333333333333,
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
                "value": 2.0,
                "unit": "m",
                "symbol": "l"
              }
            ],
            "result": {
              "value": 1.3333333333333333,
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
                "value": 4.0,
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
                "value": 1.3333333333333333,
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
                "value": 4.0,
                "unit": "m2",
                "symbol": "A"
              }
            ],
            "result": {
              "value": 680.0,
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
                "value": 4.0,
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
                "value": 1.3333333333333333,
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
                "value": 600.0,
                "unit": "kN",
                "symbol": "N"
              },
              {
                "value": 4.0,
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
                "value": 1.3333333333333333,
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
                "value": 680.0,
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
                "value": 4.0,
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
                "value": 1.3333333333333333,
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
                "value": 600.0,
                "unit": "kN",
                "symbol": "N"
              },
              {
                "value": 4.0,
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
                "value": 1.3333333333333333,
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
                "value": 680.0,
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
            "step_id": "corner_component_pp",
            "expression": "P_{\\max}=\\frac{N}{A}+\\gamma_{mt}d+\\frac{M_x}{W_x}+\\frac{M_y}{W_y}",
            "substitutions": [
              {
                "value": 600.0,
                "unit": "kN",
                "symbol": "N"
              },
              {
                "value": 4.0,
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
                "value": 1.3333333333333333,
                "unit": "m3",
                "symbol": "W_x"
              },
              {
                "value": 0.0,
                "unit": "kN*m",
                "symbol": "M_y"
              },
              {
                "value": 1.3333333333333333,
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
                "value": 1.3333333333333333,
                "unit": "m3",
                "symbol": "Wx"
              },
              {
                "value": 0.0,
                "unit": "kN*m",
                "symbol": "My_base"
              },
              {
                "value": 1.3333333333333333,
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
                "value": 600.0,
                "unit": "kN",
                "symbol": "N"
              },
              {
                "value": 4.0,
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
                "value": 1.3333333333333333,
                "unit": "m3",
                "symbol": "W_x"
              },
              {
                "value": -0.0,
                "unit": "kN*m",
                "symbol": "M_y"
              },
              {
                "value": 1.3333333333333333,
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
                "value": 1.3333333333333333,
                "unit": "m3",
                "symbol": "Wx"
              },
              {
                "value": 0.0,
                "unit": "kN*m",
                "symbol": "My_base"
              },
              {
                "value": 1.3333333333333333,
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
                "value": 600.0,
                "unit": "kN",
                "symbol": "N"
              },
              {
                "value": 4.0,
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
                "value": 1.3333333333333333,
                "unit": "m3",
                "symbol": "W_x"
              },
              {
                "value": 0.0,
                "unit": "kN*m",
                "symbol": "M_y"
              },
              {
                "value": 1.3333333333333333,
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
                "value": 1.3333333333333333,
                "unit": "m3",
                "symbol": "Wx"
              },
              {
                "value": 0.0,
                "unit": "kN*m",
                "symbol": "My_base"
              },
              {
                "value": 1.3333333333333333,
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
                "value": 600.0,
                "unit": "kN",
                "symbol": "N"
              },
              {
                "value": 4.0,
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
                "value": 1.3333333333333333,
                "unit": "m3",
                "symbol": "W_x"
              },
              {
                "value": -0.0,
                "unit": "kN*m",
                "symbol": "M_y"
              },
              {
                "value": 1.3333333333333333,
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
                "value": 1.3333333333333333,
                "unit": "m3",
                "symbol": "Wx"
              },
              {
                "value": 0.0,
                "unit": "kN*m",
                "symbol": "My_base"
              },
              {
                "value": 1.3333333333333333,
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
        "result_id": "dec00000-0000-4000-8000-000000000008",
        "parameter_source": {
          "kind": "interim",
          "data_sha256": "faaa0724af57ca6c8066f558c4e75c2785d099b34cbfb07c4a85892fdc3b68fe", // pragma: allowlist secret
          "profile": "strict"
        }
      },
      "reason": null
    }
  ],
  "stop_reason": null,
  "selected_candidate_index": null,
  "selected_result_id": null
} satisfies components['schemas']['FoundationSelectionResult']
export const selectionIncomplete = {
  "schema_version": "foundation-selection-result-v1",
  "selection_id": "dec00000-0000-4000-8000-000000000010",
  "input_hash": "0be16c70dd49b522a6edc1eead7c67026454fc8bc94334e2e0229ad13b81bf94", // pragma: allowlist secret
  "request": {
    "schema_version": "foundation-selection-request-v1",
    "calculation_type": "foundations_shallow_loads",
    "policy_version": "foundation-min-area-v1",
    "common_inputs": {
      "d_1": {
        "value": 1.0,
        "unit": "m"
      },
      "d_b": {
        "value": 0.0,
        "unit": "m"
      },
      "gamma_II": {
        "value": 20.0,
        "unit": "kN/m3"
      },
      "gamma_II_prime": {
        "value": 20.0,
        "unit": "kN/m3"
      },
      "c_II": {
        "value": 10.0,
        "unit": "kPa"
      },
      "phi_II": {
        "value": 20.0,
        "unit": "deg"
      },
      "h": {
        "value": 1.0,
        "unit": "m"
      },
      "d": {
        "value": 1.0,
        "unit": "m"
      },
      "N": {
        "value": 600.0,
        "unit": "kN"
      },
      "Mx": {
        "value": 0.0,
        "unit": "kN*m"
      },
      "My": {
        "value": 0.0,
        "unit": "kN*m"
      },
      "Qx": {
        "value": 0.0,
        "unit": "kN"
      },
      "Qy": {
        "value": 0.0,
        "unit": "kN"
      }
    },
    "candidates": [
      {
        "b": {
          "value": 2.0,
          "unit": "m"
        },
        "l": {
          "value": 3.0,
          "unit": "m"
        }
      }
    ]
  },
  "status": "incomplete",
  "outcomes": [
    {
      "index": 0,
      "candidate": {
        "b": {
          "value": 2.0,
          "unit": "m"
        },
        "l": {
          "value": 3.0,
          "unit": "m"
        }
      },
      "status": "skipped",
      "envelope": null,
      "reason": "time_budget"
    }
  ],
  "stop_reason": "time_budget",
  "selected_candidate_index": null,
  "selected_result_id": null
} satisfies components['schemas']['FoundationSelectionResult']
export const loadsCentralContext = {
  "status": "available",
  "context": {
    "schema_version": "foundation-result-context-v1",
    "result_id": "55555555-5555-4555-8555-555555555555",
    "calculation_type": "foundations_shallow_loads",
    "methodology_version": "rectangular-full-contact-v1",
    "input_hash": "22c0d8c6334ed14ddcc4f326eda3c8c7f7fc740a1c4890f4fb269ad45be4a552", // pragma: allowlist secret
    "load_level": "upper_cut",
    "weight_mode": "averaged",
    "inputs": {
      "b": {
        "value": 2.0,
        "unit": "m"
      },
      "d_1": {
        "value": 1.0,
        "unit": "m"
      },
      "d_b": {
        "value": 0.0,
        "unit": "m"
      },
      "gamma_II": {
        "value": 20.0,
        "unit": "kN/m3"
      },
      "gamma_II_prime": {
        "value": 20.0,
        "unit": "kN/m3"
      },
      "c_II": {
        "value": 10.0,
        "unit": "kPa"
      },
      "phi_II": {
        "value": 20.0,
        "unit": "deg"
      },
      "l": {
        "value": 3.0,
        "unit": "m"
      },
      "h": {
        "value": 1.0,
        "unit": "m"
      },
      "d": {
        "value": 1.0,
        "unit": "m"
      },
      "N": {
        "value": 600.0,
        "unit": "kN"
      },
      "Mx": {
        "value": 0.0,
        "unit": "kN*m"
      },
      "My": {
        "value": 0.0,
        "unit": "kN*m"
      },
      "Qx": {
        "value": 0.0,
        "unit": "kN"
      },
      "Qy": {
        "value": 0.0,
        "unit": "kN"
      }
    },
    "geometry": {
      "b": {
        "value": 2.0,
        "unit": "m"
      },
      "l": {
        "value": 3.0,
        "unit": "m"
      },
      "A": {
        "value": 6.0,
        "unit": "m2"
      },
      "Wx": {
        "value": 2.0,
        "unit": "m3"
      },
      "Wy": {
        "value": 3.0,
        "unit": "m3"
      }
    },
    "trace_values": {
      "gamma_c1": {
        "value": 1.1,
        "unit": "1"
      },
      "gamma_c2": {
        "value": 1.0,
        "unit": "1"
      },
      "k": {
        "value": 1.0,
        "unit": "1"
      },
      "M_gamma": {
        "value": 0.51,
        "unit": "1"
      },
      "M_q": {
        "value": 3.06,
        "unit": "1"
      },
      "M_c": {
        "value": 5.66,
        "unit": "1"
      },
      "k_z": {
        "value": 1.0,
        "unit": "1"
      },
      "R": {
        "value": 152.02,
        "unit": "kPa"
      },
      "A": {
        "value": 6.0,
        "unit": "m2"
      },
      "Wx": {
        "value": 2.0,
        "unit": "m3"
      },
      "Wy": {
        "value": 3.0,
        "unit": "m3"
      },
      "Mx_base": {
        "value": 0.0,
        "unit": "kN*m"
      },
      "My_base": {
        "value": 0.0,
        "unit": "kN*m"
      },
      "gamma_mt": {
        "value": 20.0,
        "unit": "kN/m3"
      },
      "p": {
        "value": 120.0,
        "unit": "kPa"
      },
      "V": {
        "value": 720.0,
        "unit": "kN"
      },
      "p_x_min": {
        "value": 120.0,
        "unit": "kPa"
      },
      "p_x_max": {
        "value": 120.0,
        "unit": "kPa"
      },
      "e_x": {
        "value": 0.0,
        "unit": "m"
      },
      "relative_eccentricity_x": {
        "value": 1.0,
        "unit": "1"
      },
      "pressure_diagram_x": {
        "value": 0.0,
        "unit": "m"
      },
      "p_y_min": {
        "value": 120.0,
        "unit": "kPa"
      },
      "p_y_max": {
        "value": 120.0,
        "unit": "kPa"
      },
      "e_y": {
        "value": 0.0,
        "unit": "m"
      },
      "relative_eccentricity_y": {
        "value": 1.0,
        "unit": "1"
      },
      "pressure_diagram_y": {
        "value": 0.0,
        "unit": "m"
      },
      "corner_component_pp": {
        "value": 120.0,
        "unit": "kPa"
      },
      "p_corner_pp": {
        "value": 120.0,
        "unit": "kPa"
      },
      "corner_component_pm": {
        "value": 120.0,
        "unit": "kPa"
      },
      "p_corner_pm": {
        "value": 120.0,
        "unit": "kPa"
      },
      "corner_component_mp": {
        "value": 120.0,
        "unit": "kPa"
      },
      "p_corner_mp": {
        "value": 120.0,
        "unit": "kPa"
      },
      "corner_component_mm": {
        "value": 120.0,
        "unit": "kPa"
      },
      "p_corner_mm": {
        "value": 120.0,
        "unit": "kPa"
      },
      "p_corner_min": {
        "value": 120.0,
        "unit": "kPa"
      },
      "p_corner_max": {
        "value": 120.0,
        "unit": "kPa"
      },
      "edge_limit_multiplier": {
        "value": 1.2,
        "unit": "1"
      },
      "edge_limit": {
        "value": 182.424,
        "unit": "kPa"
      },
      "corner_limit_multiplier": {
        "value": 1.5,
        "unit": "1"
      },
      "corner_limit": {
        "value": 228.03000000000003,
        "unit": "kPa"
      },
      "p_le_R": {
        "value": 120.0,
        "unit": "kPa"
      },
      "p_x_max_le_limit": {
        "value": 120.0,
        "unit": "kPa"
      },
      "p_y_max_le_limit": {
        "value": 120.0,
        "unit": "kPa"
      },
      "p_corner_max_le_limit": {
        "value": 120.0,
        "unit": "kPa"
      }
    },
    "pressure_state": "full_contact",
    "corners": [
      {
        "name": "pp",
        "x": {
          "value": 1.0,
          "unit": "m"
        },
        "y": {
          "value": 1.5,
          "unit": "m"
        },
        "pressure": {
          "value": 120.0,
          "unit": "kPa"
        },
        "step_id": "p_corner_pp"
      },
      {
        "name": "pm",
        "x": {
          "value": 1.0,
          "unit": "m"
        },
        "y": {
          "value": -1.5,
          "unit": "m"
        },
        "pressure": {
          "value": 120.0,
          "unit": "kPa"
        },
        "step_id": "p_corner_pm"
      },
      {
        "name": "mp",
        "x": {
          "value": -1.0,
          "unit": "m"
        },
        "y": {
          "value": 1.5,
          "unit": "m"
        },
        "pressure": {
          "value": 120.0,
          "unit": "kPa"
        },
        "step_id": "p_corner_mp"
      },
      {
        "name": "mm",
        "x": {
          "value": -1.0,
          "unit": "m"
        },
        "y": {
          "value": -1.5,
          "unit": "m"
        },
        "pressure": {
          "value": 120.0,
          "unit": "kPa"
        },
        "step_id": "p_corner_mm"
      }
    ]
  }
} satisfies components['schemas']['FoundationContextResponse']
export const loadsContactRefusalContext = {
  "status": "available",
  "context": {
    "schema_version": "foundation-result-context-v1",
    "result_id": "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa",
    "calculation_type": "foundations_shallow_loads",
    "methodology_version": "rectangular-full-contact-v1",
    "input_hash": "f4b13a8543416777e9a56a89b3e498631219a7ef77ceff19a3a9b5da628076b5", // pragma: allowlist secret
    "load_level": "upper_cut",
    "weight_mode": "averaged",
    "inputs": {
      "b": {
        "value": 2.0,
        "unit": "m"
      },
      "d_1": {
        "value": 1.0,
        "unit": "m"
      },
      "d_b": {
        "value": 0.0,
        "unit": "m"
      },
      "gamma_II": {
        "value": 20.0,
        "unit": "kN/m3"
      },
      "gamma_II_prime": {
        "value": 20.0,
        "unit": "kN/m3"
      },
      "c_II": {
        "value": 10.0,
        "unit": "kPa"
      },
      "phi_II": {
        "value": 20.0,
        "unit": "deg"
      },
      "l": {
        "value": 3.0,
        "unit": "m"
      },
      "h": {
        "value": 1.0,
        "unit": "m"
      },
      "d": {
        "value": 1.0,
        "unit": "m"
      },
      "N": {
        "value": 600.0,
        "unit": "kN"
      },
      "Mx": {
        "value": 180.0,
        "unit": "kN*m"
      },
      "My": {
        "value": 180.0,
        "unit": "kN*m"
      },
      "Qx": {
        "value": 0.0,
        "unit": "kN"
      },
      "Qy": {
        "value": 0.0,
        "unit": "kN"
      }
    },
    "geometry": {
      "b": {
        "value": 2.0,
        "unit": "m"
      },
      "l": {
        "value": 3.0,
        "unit": "m"
      },
      "A": {
        "value": 6.0,
        "unit": "m2"
      },
      "Wx": {
        "value": 2.0,
        "unit": "m3"
      },
      "Wy": {
        "value": 3.0,
        "unit": "m3"
      }
    },
    "trace_values": {
      "gamma_c1": {
        "value": 1.1,
        "unit": "1"
      },
      "gamma_c2": {
        "value": 1.0,
        "unit": "1"
      },
      "k": {
        "value": 1.0,
        "unit": "1"
      },
      "M_gamma": {
        "value": 0.51,
        "unit": "1"
      },
      "M_q": {
        "value": 3.06,
        "unit": "1"
      },
      "M_c": {
        "value": 5.66,
        "unit": "1"
      },
      "k_z": {
        "value": 1.0,
        "unit": "1"
      },
      "R": {
        "value": 152.02,
        "unit": "kPa"
      },
      "A": {
        "value": 6.0,
        "unit": "m2"
      },
      "Wx": {
        "value": 2.0,
        "unit": "m3"
      },
      "Wy": {
        "value": 3.0,
        "unit": "m3"
      },
      "Mx_base": {
        "value": 180.0,
        "unit": "kN*m"
      },
      "My_base": {
        "value": 180.0,
        "unit": "kN*m"
      },
      "gamma_mt": {
        "value": 20.0,
        "unit": "kN/m3"
      },
      "p": {
        "value": 120.0,
        "unit": "kPa"
      },
      "V": {
        "value": 720.0,
        "unit": "kN"
      },
      "p_x_min": {
        "value": 30.0,
        "unit": "kPa"
      },
      "p_x_max": {
        "value": 210.0,
        "unit": "kPa"
      },
      "e_x": {
        "value": 0.25,
        "unit": "m"
      },
      "relative_eccentricity_x": {
        "value": 1.0,
        "unit": "1"
      },
      "pressure_diagram_x": {
        "value": 0.25,
        "unit": "m"
      },
      "p_y_min": {
        "value": 60.0,
        "unit": "kPa"
      },
      "p_y_max": {
        "value": 180.0,
        "unit": "kPa"
      },
      "e_y": {
        "value": 0.25,
        "unit": "m"
      },
      "relative_eccentricity_y": {
        "value": 1.0,
        "unit": "1"
      },
      "pressure_diagram_y": {
        "value": 0.25,
        "unit": "m"
      },
      "corner_component_pp": {
        "value": 270.0,
        "unit": "kPa"
      },
      "p_corner_pp": {
        "value": 270.0,
        "unit": "kPa"
      },
      "corner_component_pm": {
        "value": 150.0,
        "unit": "kPa"
      },
      "p_corner_pm": {
        "value": 150.0,
        "unit": "kPa"
      },
      "corner_component_mp": {
        "value": 90.0,
        "unit": "kPa"
      },
      "p_corner_mp": {
        "value": 90.0,
        "unit": "kPa"
      },
      "corner_component_mm": {
        "value": -30.0,
        "unit": "kPa"
      },
      "p_corner_mm": {
        "value": -30.0,
        "unit": "kPa"
      },
      "p_corner_min": {
        "value": -30.0,
        "unit": "kPa"
      },
      "p_corner_max": {
        "value": 270.0,
        "unit": "kPa"
      }
    },
    "pressure_state": "diagnostic",
    "corners": [
      {
        "name": "pp",
        "x": {
          "value": 1.0,
          "unit": "m"
        },
        "y": {
          "value": 1.5,
          "unit": "m"
        },
        "pressure": {
          "value": 270.0,
          "unit": "kPa"
        },
        "step_id": "p_corner_pp"
      },
      {
        "name": "pm",
        "x": {
          "value": 1.0,
          "unit": "m"
        },
        "y": {
          "value": -1.5,
          "unit": "m"
        },
        "pressure": {
          "value": 150.0,
          "unit": "kPa"
        },
        "step_id": "p_corner_pm"
      },
      {
        "name": "mp",
        "x": {
          "value": -1.0,
          "unit": "m"
        },
        "y": {
          "value": 1.5,
          "unit": "m"
        },
        "pressure": {
          "value": 90.0,
          "unit": "kPa"
        },
        "step_id": "p_corner_mp"
      },
      {
        "name": "mm",
        "x": {
          "value": -1.0,
          "unit": "m"
        },
        "y": {
          "value": -1.5,
          "unit": "m"
        },
        "pressure": {
          "value": -30.0,
          "unit": "kPa"
        },
        "step_id": "p_corner_mm"
      }
    ]
  }
} satisfies components['schemas']['FoundationContextResponse']
