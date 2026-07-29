import { getAttackLabel } from "../../utils/attackLabels";
import Panel from "../common/Panel";

function SelectTypePacketSection({
    labels,
    selectedAttack,
    setSelectedAttack,
}) {
    return (

        <Panel
            className="
                relative
                w-[215px]
                h-[322px]
            "
        >

            {/* ================= Title ================= */}

            <h2
                className="
                    absolute
                    text-[16px]
                    font-bold
                "
                style={{
                    left: "16px",
                    top: "14px",
                }}
            >
                SELECT TYPE PACKET
            </h2>

            <div
                className="absolute"
                style={{
                    left: "16px",
                    top: "51px",
                }}
            >

                {
                    labels.map((label, index) => (

                        <div
                            key={label}
                            className="cursor-pointer"
                            onClick={() => setSelectedAttack(label)}
                            style={{
                                marginBottom: "24px",
                                width: "170px",
                                position: "relative",
                            }}
                        >

                            <span
                                className="
                                    text-[14px]
                                    font-bold
                                    whitespace-nowrap
                                "
                            >
                                {label.toUpperCase()}

                                <span
                                    className="
                                        text-[8px]
                                        font-normal
                                        text-gray-300
                                        ml-[4px]
                                    "
                                >
                                    ({getAttackLabel(label)})
                                </span>

                            </span>

                            <button
                                className="
                                    absolute
                                    right-0
                                    top-0
                                    w-[20px]
                                    h-[20px]
                                    rounded-full
                                    border
                                    border-white
                                "
                                style={{
                                    backgroundColor:
                                        selectedAttack === label
                                            ? "#FF1A1A"
                                            : "#FFFFFF",
                                }}
                            />

                        </div>

                    ))
                }

            </div>

        </Panel>

    );
}

export default SelectTypePacketSection;