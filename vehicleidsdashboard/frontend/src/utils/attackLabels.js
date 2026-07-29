export const ATTACK_LABELS = {

    "C_D": "CAN DoS",

    "C_R": "CAN Replay",

    "F_I": "Fuzzy Injection",

    "M_F": "MAC Flooding",

    "P_I": "gPTP Synchronization Attack",

    "Normal": "Normal",

};

export function getAttackLabel(label) {

    return ATTACK_LABELS[label] ?? label;

}