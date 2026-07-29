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
    const fillWidth = `${value}%`;

    return (

        <div
            className="
                absolute
                flex
                items-center
            "
            style={{
                left: "414px",
                right: "20px",
                top,
                height: "12px",
            }}
        >

            {/* Label */}
            <span
                className="
                    w-[95px]
                    text-[10px]
                    shrink-0
                "
            >
                {displayName}
            </span>

            {/* Background Bar */}
            <div
                className="
                    flex-1
                    h-[12px]
                    rounded-full
                    mx-[10px]
                "
                style={{
                    background:"#29354E"
                }}
            >

                {/* Value Bar */}
                <div
                    className="h-full rounded-full"
                    style={{
                        width: fillWidth,
                        background: color,
                    }}
                />

            </div>

            {/* Percentage */}
            <span
                className="
                    w-[48px]
                    text-right
                    text-[10px]
                    shrink-0
                "
            >
                {value.toFixed(2)}%
            </span>

        </div>

    );

}

export default ProbabilityBar;