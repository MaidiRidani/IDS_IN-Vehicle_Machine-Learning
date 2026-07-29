import Panel from "../common/Panel";
function SummarySection({
    configurations,
    editingPacket,
    onSelectConfiguration,
    onDeleteConfiguration,
}) {
    console.log("sumary",configurations);
    console.log(Array.isArray("Sumary",configurations));
    return (

        <Panel
            className="
                relative
                w-[356px]
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
                    left: "12px",
                    top: "9px",
                }}
            >
                SUMMARY
            </h2>

            {/* ================= Table ================= */}

            <div
                className="
                    absolute
                    w-[356px]
                    h-[260px]
                    overflow-y-auto
                "
                style={{
                    left: "0px",
                    top: "36px",
                }}
            >

                <table className="w-full text-[12px]">

                    {/* Header (tetap) */}

                    <thead
                        className="
                            sticky
                            top-0
                            bg-[#6905FE]
                            z-10
                        "
                    >
                        <tr
                            className="
                                text-left
                                font-bold
                            "
                        >
                            <th className="pl-[12px] py-[10px] w-[40px]">
                                NO
                            </th>

                            <th className="w-[120px]">
                                PACKET
                            </th>

                            <th className="pl-[8px] w-[135px]">
                                TYPE
                            </th>

                            <th className="w-[70px]">
                                POSITION WINDOW
                            </th>

                            <th className="w-[35px] text-center">
                                DEL
                            </th>
                        </tr>
                    </thead>

                    {/* Body */}
                    <tbody>

                        {configurations.map((config, index) => (

                            <tr
                                key={config.packet_number}
                                className={`
                                    h-[34px]
                                    cursor-pointer
                                    hover:bg-[#1E3A8A]
                                    ${
                                        editingPacket === config.packet_number
                                            ? "bg-[#2563EB]"
                                            : ""
                                    }
                                `}
                                onClick={() => onSelectConfiguration(config)}
                            >

                                <td className="pl-[12px]">
                                    {index + 1}
                                </td>

                                <td>
                                    Packet #{config.packet_number}
                                </td>

                                <td>
                                    {config.attack_type}
                                </td>

                                <td>
                                    {config.position}
                                </td>

                                <td className="text-center">

                                    <button
                                        onClick={(e) => {

                                            e.stopPropagation();

                                            onDeleteConfiguration(
                                                config.packet_number
                                            );

                                        }}
                                    >
                                        ✕
                                    </button>

                                </td>

                            </tr>

                        ))}

                    </tbody>

                </table>

            </div>

        </Panel>

    );
}

export default SummarySection;