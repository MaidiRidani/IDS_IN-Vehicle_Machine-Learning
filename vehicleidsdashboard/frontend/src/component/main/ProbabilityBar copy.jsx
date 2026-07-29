import { CLASS_INFO } from "../../constants/classInfo";


function ProbabilityBar({
    label,
    value,
    top,
}) {

    const classInfo = CLASS_INFO[label];

    const displayName = classInfo?.displayName ?? label;

    const color = classInfo?.color ?? "#FFFFFF";


    const CLASS_COLORS = {

        Normal: "#00FF11",

        F_I: "#6905FE",

        P_I: "#EEFF00",

        M_F: "#FF8000",

        C_D: "#BB00FF",

        C_R: "#FF0000",

    };

    // Lebar recnil (maksimum 108 px)
    const fillWidth = (value / 100) * 108;

    return (

        <div
            className="absolute"
            style={{
                left: "414px",
                top,
                width: "240px",
                height: "12px",
            }}
        >

            {/* Label */}
            <span
                className="absolute text-[10px] font-normal"
                style={{
                    left: "0px",
                    top: "0px",
                    width: "95px",      // Kolom label tetap
                }}
            >
                {displayName}
            </span>

            {/* Background Bar */}
            <div
                className="absolute w-[108px] h-[12px] rounded-full"
                style={{
                    left: "105px",      // Semua bar mulai di titik yang sama
                    top: "0px",
                    background: "#29354E",
                }}
            >

                {/* Value Bar */}
                <div
                    className="h-full rounded-full"
                    style={{
                        width: `${fillWidth}px`,
                        background: color,
                    }}
                />

            </div>

            {/* Percentage */}
            <span
                className="absolute text-[10px] font-normal"
                style={{
                    left: "217px",      // Semua persen mulai di titik yang sama
                    top: "0px",
                    width: "45px",
                }}
            >
                {value.toFixed(2)}%
            </span>

        </div>

    );

}

export default ProbabilityBar;