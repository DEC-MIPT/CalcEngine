import type { components } from '../api/schema'

type CalculationTypeView = components['schemas']['CalculationTypeView']
type ResultEnvelope = components['schemas']['ResultEnvelope']

export const PASS_ID = '11111111-1111-4111-8111-111111111111'
export const FAIL_ID = '22222222-2222-4222-8222-222222222222'
export const REFUSED_ID = '33333333-3333-4333-8333-333333333333'
export const WARNING_ID = '44444444-4444-4444-8444-444444444444'

export const calculationTypes = [
  {
    "name": "foundations_shallow_r",
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
        "name": "p",
        "base_unit": "kPa",
        "dimension": "pressure",
        "units": [
          "Pa",
          "kPa",
          "MPa"
        ],
        "label": {
          "ru": "Среднее давление под подошвой",
          "en": "Average pressure under the base"
        },
        "symbol": "p",
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
          "en": "Design soil resistance"
        },
        "symbol": "R"
      }
    ]
  }
] satisfies CalculationTypeView[]

export const passEnvelope = {
  "engine_version": "0.1.0",
  "engineer_rules": [
    {
      "engineer": "<ENGINEER>",
      "rationale": "<RATIONALE>"
    }
  ],
  "input_hash": "193f19fc07f1b2175bb4f0afa61a9f6c3224c678c0bb4e37a7c769b5abe0771e", // pragma: allowlist secret
  "norm_refs": [
    {
      "clause": "<CLAUSE-PLACEHOLDER>",
      "document": "<NORM-DOC-PLACEHOLDER>",
      "edition": "unverified",
      "provenance": "machine-extracted",
      "status": "unverified"
    }
  ],
  "outputs": [
    {
      "quantity": "R",
      "rounding_rule": {
        "decimals": 1,
        "mode": "half_up"
      },
      "rounding_source": {
        "engineer": "<ENGINEER>",
        "rationale": "<RATIONALE>"
      },
      "unit": "kPa",
      "value": 172.5
    }
  ],
  "trace": [
    {
      "expression": "gamma_c1",
      "kind": "table",
      "norm_refs": [
        {
          "clause": "<CLAUSE-PLACEHOLDER>",
          "document": "<NORM-DOC-PLACEHOLDER>",
          "edition": "unverified",
          "provenance": "machine-extracted",
          "status": "unverified"
        }
      ],
      "result": {
        "unit": "1",
        "value": 2.0
      },
      "step_id": "gamma_c1",
      "substitutions": []
    },
    {
      "expression": "gamma_c2",
      "kind": "table",
      "norm_refs": [
        {
          "clause": "<CLAUSE-PLACEHOLDER>",
          "document": "<NORM-DOC-PLACEHOLDER>",
          "edition": "unverified",
          "provenance": "machine-extracted",
          "status": "unverified"
        }
      ],
      "result": {
        "unit": "1",
        "value": 3.0
      },
      "step_id": "gamma_c2",
      "substitutions": []
    },
    {
      "expression": "k",
      "kind": "table",
      "norm_refs": [
        {
          "clause": "<CLAUSE-PLACEHOLDER>",
          "document": "<NORM-DOC-PLACEHOLDER>",
          "edition": "unverified",
          "provenance": "machine-extracted",
          "status": "unverified"
        }
      ],
      "result": {
        "unit": "1",
        "value": 4.0
      },
      "step_id": "k",
      "substitutions": []
    },
    {
      "expression": "M_gamma = M_gamma\\left(phi_II\\right)",
      "kind": "table",
      "norm_refs": [
        {
          "clause": "<CLAUSE-PLACEHOLDER>",
          "document": "<NORM-DOC-PLACEHOLDER>",
          "edition": "unverified",
          "provenance": "machine-extracted",
          "status": "unverified"
        }
      ],
      "result": {
        "unit": "1",
        "value": 0.5
      },
      "step_id": "M_gamma",
      "substitutions": [
        {
          "symbol": "phi_II",
          "unit": "deg",
          "value": 20.0
        }
      ]
    },
    {
      "expression": "M_q = M_q\\left(phi_II\\right)",
      "kind": "table",
      "norm_refs": [
        {
          "clause": "<CLAUSE-PLACEHOLDER>",
          "document": "<NORM-DOC-PLACEHOLDER>",
          "edition": "unverified",
          "provenance": "machine-extracted",
          "status": "unverified"
        }
      ],
      "result": {
        "unit": "1",
        "value": 5.0
      },
      "step_id": "M_q",
      "substitutions": [
        {
          "symbol": "phi_II",
          "unit": "deg",
          "value": 20.0
        }
      ]
    },
    {
      "expression": "M_c = M_c\\left(phi_II\\right)",
      "kind": "table",
      "norm_refs": [
        {
          "clause": "<CLAUSE-PLACEHOLDER>",
          "document": "<NORM-DOC-PLACEHOLDER>",
          "edition": "unverified",
          "provenance": "machine-extracted",
          "status": "unverified"
        }
      ],
      "result": {
        "unit": "1",
        "value": 10.0
      },
      "step_id": "M_c",
      "substitutions": [
        {
          "symbol": "phi_II",
          "unit": "deg",
          "value": 20.0
        }
      ]
    },
    {
      "expression": "k_z = \\kappa",
      "kind": "formula",
      "norm_refs": [
        {
          "clause": "<CLAUSE-PLACEHOLDER>",
          "document": "<NORM-DOC-PLACEHOLDER>",
          "edition": "unverified",
          "provenance": "machine-extracted",
          "status": "unverified"
        }
      ],
      "result": {
        "unit": "1",
        "value": 3.0
      },
      "step_id": "k_z",
      "substitutions": []
    },
    {
      "expression": "R = \\mathrm{synthetic}",
      "kind": "formula",
      "norm_refs": [
        {
          "clause": "<CLAUSE-PLACEHOLDER>",
          "document": "<NORM-DOC-PLACEHOLDER>",
          "edition": "unverified",
          "provenance": "machine-extracted",
          "status": "unverified"
        }
      ],
      "result": {
        "unit": "kPa",
        "value": 172.5
      },
      "step_id": "R",
      "substitutions": [
        {
          "symbol": "gamma_c1",
          "unit": "1",
          "value": 2.0
        },
        {
          "symbol": "c_II",
          "unit": "kPa",
          "value": 3.0
        },
        {
          "symbol": "M_c",
          "unit": "1",
          "value": 10.0
        },
        {
          "symbol": "gamma_c2",
          "unit": "1",
          "value": 3.0
        },
        {
          "symbol": "M_q",
          "unit": "1",
          "value": 5.0
        },
        {
          "symbol": "d_1",
          "unit": "m",
          "value": 1.0
        },
        {
          "symbol": "gamma_II_prime",
          "unit": "kN/m3",
          "value": 20.0
        },
        {
          "symbol": "k",
          "unit": "1",
          "value": 4.0
        },
        {
          "symbol": "M_gamma",
          "unit": "1",
          "value": 0.5
        },
        {
          "symbol": "k_z",
          "unit": "1",
          "value": 3.0
        },
        {
          "symbol": "b",
          "unit": "m",
          "value": 2.0
        },
        {
          "symbol": "d_b",
          "unit": "m",
          "value": 0.5
        },
        {
          "symbol": "gamma_II",
          "unit": "kN/m3",
          "value": 10.0
        }
      ]
    },
    {
      "expression": "p \\le R",
      "kind": "check",
      "norm_refs": [
        {
          "clause": "<CLAUSE-PLACEHOLDER>",
          "document": "<NORM-DOC-PLACEHOLDER>",
          "edition": "unverified",
          "provenance": "machine-extracted",
          "status": "unverified"
        }
      ],
      "operator": "le",
      "passed": true,
      "result": {
        "unit": "kPa",
        "value": 100.0
      },
      "right": {
        "unit": "kPa",
        "value": 172.5
      },
      "step_id": "p_le_R",
      "substitutions": [
        {
          "symbol": "p",
          "unit": "kPa",
          "value": 100.0
        },
        {
          "symbol": "R",
          "unit": "kPa",
          "value": 172.5
        }
      ]
    }
  ],
  "unverified_step_count": 9,
  "verdict": "pass",
  "verdict_reason": {
    "kind": "check",
    "step_id": "p_le_R"
  },
  "warnings": [],
  "result_id": "11111111-1111-4111-8111-111111111111"
} satisfies ResultEnvelope

export const failEnvelope = {
  "engine_version": "0.1.0",
  "engineer_rules": [
    {
      "engineer": "<ENGINEER>",
      "rationale": "<RATIONALE>"
    }
  ],
  "input_hash": "325b2bd7e2a18566150a9b015926b0e6340ff7cd57259a5f157e9bb269d85e35", // pragma: allowlist secret
  "norm_refs": [
    {
      "clause": "<CLAUSE-PLACEHOLDER>",
      "document": "<NORM-DOC-PLACEHOLDER>",
      "edition": "unverified",
      "provenance": "machine-extracted",
      "status": "unverified"
    }
  ],
  "outputs": [
    {
      "quantity": "R",
      "rounding_rule": {
        "decimals": 1,
        "mode": "half_up"
      },
      "rounding_source": {
        "engineer": "<ENGINEER>",
        "rationale": "<RATIONALE>"
      },
      "unit": "kPa",
      "value": 172.5
    }
  ],
  "trace": [
    {
      "expression": "gamma_c1",
      "kind": "table",
      "norm_refs": [
        {
          "clause": "<CLAUSE-PLACEHOLDER>",
          "document": "<NORM-DOC-PLACEHOLDER>",
          "edition": "unverified",
          "provenance": "machine-extracted",
          "status": "unverified"
        }
      ],
      "result": {
        "unit": "1",
        "value": 2.0
      },
      "step_id": "gamma_c1",
      "substitutions": []
    },
    {
      "expression": "gamma_c2",
      "kind": "table",
      "norm_refs": [
        {
          "clause": "<CLAUSE-PLACEHOLDER>",
          "document": "<NORM-DOC-PLACEHOLDER>",
          "edition": "unverified",
          "provenance": "machine-extracted",
          "status": "unverified"
        }
      ],
      "result": {
        "unit": "1",
        "value": 3.0
      },
      "step_id": "gamma_c2",
      "substitutions": []
    },
    {
      "expression": "k",
      "kind": "table",
      "norm_refs": [
        {
          "clause": "<CLAUSE-PLACEHOLDER>",
          "document": "<NORM-DOC-PLACEHOLDER>",
          "edition": "unverified",
          "provenance": "machine-extracted",
          "status": "unverified"
        }
      ],
      "result": {
        "unit": "1",
        "value": 4.0
      },
      "step_id": "k",
      "substitutions": []
    },
    {
      "expression": "M_gamma = M_gamma\\left(phi_II\\right)",
      "kind": "table",
      "norm_refs": [
        {
          "clause": "<CLAUSE-PLACEHOLDER>",
          "document": "<NORM-DOC-PLACEHOLDER>",
          "edition": "unverified",
          "provenance": "machine-extracted",
          "status": "unverified"
        }
      ],
      "result": {
        "unit": "1",
        "value": 0.5
      },
      "step_id": "M_gamma",
      "substitutions": [
        {
          "symbol": "phi_II",
          "unit": "deg",
          "value": 20.0
        }
      ]
    },
    {
      "expression": "M_q = M_q\\left(phi_II\\right)",
      "kind": "table",
      "norm_refs": [
        {
          "clause": "<CLAUSE-PLACEHOLDER>",
          "document": "<NORM-DOC-PLACEHOLDER>",
          "edition": "unverified",
          "provenance": "machine-extracted",
          "status": "unverified"
        }
      ],
      "result": {
        "unit": "1",
        "value": 5.0
      },
      "step_id": "M_q",
      "substitutions": [
        {
          "symbol": "phi_II",
          "unit": "deg",
          "value": 20.0
        }
      ]
    },
    {
      "expression": "M_c = M_c\\left(phi_II\\right)",
      "kind": "table",
      "norm_refs": [
        {
          "clause": "<CLAUSE-PLACEHOLDER>",
          "document": "<NORM-DOC-PLACEHOLDER>",
          "edition": "unverified",
          "provenance": "machine-extracted",
          "status": "unverified"
        }
      ],
      "result": {
        "unit": "1",
        "value": 10.0
      },
      "step_id": "M_c",
      "substitutions": [
        {
          "symbol": "phi_II",
          "unit": "deg",
          "value": 20.0
        }
      ]
    },
    {
      "expression": "k_z = \\kappa",
      "kind": "formula",
      "norm_refs": [
        {
          "clause": "<CLAUSE-PLACEHOLDER>",
          "document": "<NORM-DOC-PLACEHOLDER>",
          "edition": "unverified",
          "provenance": "machine-extracted",
          "status": "unverified"
        }
      ],
      "result": {
        "unit": "1",
        "value": 3.0
      },
      "step_id": "k_z",
      "substitutions": []
    },
    {
      "expression": "R = \\mathrm{synthetic}",
      "kind": "formula",
      "norm_refs": [
        {
          "clause": "<CLAUSE-PLACEHOLDER>",
          "document": "<NORM-DOC-PLACEHOLDER>",
          "edition": "unverified",
          "provenance": "machine-extracted",
          "status": "unverified"
        }
      ],
      "result": {
        "unit": "kPa",
        "value": 172.5
      },
      "step_id": "R",
      "substitutions": [
        {
          "symbol": "gamma_c1",
          "unit": "1",
          "value": 2.0
        },
        {
          "symbol": "c_II",
          "unit": "kPa",
          "value": 3.0
        },
        {
          "symbol": "M_c",
          "unit": "1",
          "value": 10.0
        },
        {
          "symbol": "gamma_c2",
          "unit": "1",
          "value": 3.0
        },
        {
          "symbol": "M_q",
          "unit": "1",
          "value": 5.0
        },
        {
          "symbol": "d_1",
          "unit": "m",
          "value": 1.0
        },
        {
          "symbol": "gamma_II_prime",
          "unit": "kN/m3",
          "value": 20.0
        },
        {
          "symbol": "k",
          "unit": "1",
          "value": 4.0
        },
        {
          "symbol": "M_gamma",
          "unit": "1",
          "value": 0.5
        },
        {
          "symbol": "k_z",
          "unit": "1",
          "value": 3.0
        },
        {
          "symbol": "b",
          "unit": "m",
          "value": 2.0
        },
        {
          "symbol": "d_b",
          "unit": "m",
          "value": 0.5
        },
        {
          "symbol": "gamma_II",
          "unit": "kN/m3",
          "value": 10.0
        }
      ]
    },
    {
      "expression": "p \\le R",
      "kind": "check",
      "norm_refs": [
        {
          "clause": "<CLAUSE-PLACEHOLDER>",
          "document": "<NORM-DOC-PLACEHOLDER>",
          "edition": "unverified",
          "provenance": "machine-extracted",
          "status": "unverified"
        }
      ],
      "operator": "le",
      "passed": false,
      "result": {
        "unit": "kPa",
        "value": 200.0
      },
      "right": {
        "unit": "kPa",
        "value": 172.5
      },
      "step_id": "p_le_R",
      "substitutions": [
        {
          "symbol": "p",
          "unit": "kPa",
          "value": 200.0
        },
        {
          "symbol": "R",
          "unit": "kPa",
          "value": 172.5
        }
      ]
    }
  ],
  "unverified_step_count": 9,
  "verdict": "fail",
  "verdict_reason": {
    "kind": "check",
    "step_id": "p_le_R"
  },
  "warnings": [],
  "result_id": "22222222-2222-4222-8222-222222222222"
} satisfies ResultEnvelope

export const refusedEnvelope = {
  "engine_version": "0.1.0",
  "input_hash": "586569603965d80d3586fcc73d817d9ab61d9f12d3cd20a679024517add1cd10", // pragma: allowlist secret
  "outputs": [],
  "norm_refs": [
    {
      "document": "<NORM-DOC-PLACEHOLDER>",
      "edition": "unverified",
      "clause": "<CLAUSE-PLACEHOLDER>",
      "status": "unverified",
      "provenance": "machine-extracted"
    }
  ],
  "engineer_rules": [],
  "verdict": "refused",
  "verdict_reason": {
    "kind": "bound",
    "value": {
      "value": 12.0,
      "unit": "m"
    },
    "bound": {
      "quantity": "b",
      "kind": "max",
      "value": 10.0,
      "inclusive": true,
      "source": [
        {
          "document": "<NORM-DOC-PLACEHOLDER>",
          "edition": "unverified",
          "clause": "<CLAUSE-PLACEHOLDER>",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ]
    }
  },
  "warnings": [],
  "trace": [],
  "unverified_step_count": 0,
  "result_id": "33333333-3333-4333-8333-333333333333"
} satisfies ResultEnvelope

export const warningEnvelope = {
  "engine_version": "0.1.0",
  "input_hash": "2f42634b24126f725dce7b86c562ecae0b2b616f9af454450f10f3e271684702", // pragma: allowlist secret
  "outputs": [
    {
      "value": 183.8,
      "unit": "kPa",
      "quantity": "R",
      "rounding_rule": {
        "decimals": 1,
        "mode": "half_up"
      },
      "rounding_source": {
        "engineer": "<ENGINEER>",
        "rationale": "<RATIONALE>"
      }
    }
  ],
  "norm_refs": [
    {
      "document": "<NORM-DOC-PLACEHOLDER>",
      "edition": "unverified",
      "clause": "<CLAUSE-PLACEHOLDER>",
      "status": "unverified",
      "provenance": "machine-extracted"
    }
  ],
  "engineer_rules": [
    {
      "engineer": "<ENGINEER>",
      "rationale": "<RATIONALE>"
    }
  ],
  "verdict": "pass",
  "verdict_reason": {
    "kind": "check",
    "step_id": "p_le_R"
  },
  "warnings": [
    {
      "value": {
        "value": 6.0,
        "unit": "m"
      },
      "bound": {
        "quantity": "b",
        "kind": "max",
        "value": 5.0,
        "inclusive": true,
        "source": {
          "engineer": "<ENGINEER>",
          "rationale": "<RATIONALE>"
        }
      }
    }
  ],
  "trace": [
    {
      "step_id": "gamma_c1",
      "expression": "gamma_c1",
      "substitutions": [],
      "result": {
        "value": 2.0,
        "unit": "1"
      },
      "norm_refs": [
        {
          "document": "<NORM-DOC-PLACEHOLDER>",
          "edition": "unverified",
          "clause": "<CLAUSE-PLACEHOLDER>",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "table"
    },
    {
      "step_id": "gamma_c2",
      "expression": "gamma_c2",
      "substitutions": [],
      "result": {
        "value": 3.0,
        "unit": "1"
      },
      "norm_refs": [
        {
          "document": "<NORM-DOC-PLACEHOLDER>",
          "edition": "unverified",
          "clause": "<CLAUSE-PLACEHOLDER>",
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
        "value": 4.0,
        "unit": "1"
      },
      "norm_refs": [
        {
          "document": "<NORM-DOC-PLACEHOLDER>",
          "edition": "unverified",
          "clause": "<CLAUSE-PLACEHOLDER>",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "table"
    },
    {
      "step_id": "M_gamma",
      "expression": "M_gamma = M_gamma\\left(phi_II\\right)",
      "substitutions": [
        {
          "value": 20.0,
          "unit": "deg",
          "symbol": "phi_II"
        }
      ],
      "result": {
        "value": 0.5,
        "unit": "1"
      },
      "norm_refs": [
        {
          "document": "<NORM-DOC-PLACEHOLDER>",
          "edition": "unverified",
          "clause": "<CLAUSE-PLACEHOLDER>",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "table"
    },
    {
      "step_id": "M_q",
      "expression": "M_q = M_q\\left(phi_II\\right)",
      "substitutions": [
        {
          "value": 20.0,
          "unit": "deg",
          "symbol": "phi_II"
        }
      ],
      "result": {
        "value": 5.0,
        "unit": "1"
      },
      "norm_refs": [
        {
          "document": "<NORM-DOC-PLACEHOLDER>",
          "edition": "unverified",
          "clause": "<CLAUSE-PLACEHOLDER>",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "table"
    },
    {
      "step_id": "M_c",
      "expression": "M_c = M_c\\left(phi_II\\right)",
      "substitutions": [
        {
          "value": 20.0,
          "unit": "deg",
          "symbol": "phi_II"
        }
      ],
      "result": {
        "value": 10.0,
        "unit": "1"
      },
      "norm_refs": [
        {
          "document": "<NORM-DOC-PLACEHOLDER>",
          "edition": "unverified",
          "clause": "<CLAUSE-PLACEHOLDER>",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "table"
    },
    {
      "step_id": "k_z",
      "expression": "k_z = b / 4",
      "substitutions": [
        {
          "value": 6.0,
          "unit": "m",
          "symbol": "b"
        }
      ],
      "result": {
        "value": 1.5,
        "unit": "1"
      },
      "norm_refs": [
        {
          "document": "<NORM-DOC-PLACEHOLDER>",
          "edition": "unverified",
          "clause": "<CLAUSE-PLACEHOLDER>",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "formula"
    },
    {
      "step_id": "R",
      "expression": "R = \\mathrm{synthetic}",
      "substitutions": [
        {
          "value": 2.0,
          "unit": "1",
          "symbol": "gamma_c1"
        },
        {
          "value": 3.0,
          "unit": "kPa",
          "symbol": "c_II"
        },
        {
          "value": 10.0,
          "unit": "1",
          "symbol": "M_c"
        },
        {
          "value": 3.0,
          "unit": "1",
          "symbol": "gamma_c2"
        },
        {
          "value": 5.0,
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
          "value": 4.0,
          "unit": "1",
          "symbol": "k"
        },
        {
          "value": 0.5,
          "unit": "1",
          "symbol": "M_gamma"
        },
        {
          "value": 1.5,
          "unit": "1",
          "symbol": "k_z"
        },
        {
          "value": 6.0,
          "unit": "m",
          "symbol": "b"
        },
        {
          "value": 0.5,
          "unit": "m",
          "symbol": "d_b"
        },
        {
          "value": 10.0,
          "unit": "kN/m3",
          "symbol": "gamma_II"
        }
      ],
      "result": {
        "value": 183.75,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "<NORM-DOC-PLACEHOLDER>",
          "edition": "unverified",
          "clause": "<CLAUSE-PLACEHOLDER>",
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
          "value": 100.0,
          "unit": "kPa",
          "symbol": "p"
        },
        {
          "value": 183.75,
          "unit": "kPa",
          "symbol": "R"
        }
      ],
      "result": {
        "value": 100.0,
        "unit": "kPa"
      },
      "norm_refs": [
        {
          "document": "<NORM-DOC-PLACEHOLDER>",
          "edition": "unverified",
          "clause": "<CLAUSE-PLACEHOLDER>",
          "status": "unverified",
          "provenance": "machine-extracted"
        }
      ],
      "kind": "check",
      "operator": "le",
      "right": {
        "value": 183.75,
        "unit": "kPa"
      },
      "passed": true
    }
  ],
  "unverified_step_count": 9,
  "result_id": "44444444-4444-4444-8444-444444444444"
} satisfies ResultEnvelope
