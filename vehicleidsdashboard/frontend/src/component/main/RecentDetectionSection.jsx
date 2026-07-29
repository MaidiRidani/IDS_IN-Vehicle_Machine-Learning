import Panel from "../common/Panel";
import { CLASS_INFO } from "../../constants/classInfo";



function RecentDetectionSection({

    history,

    className = "",

}) {

    const detections =

        [...(history ?? [])]

            .reverse()

    return (

        <Panel
            className={`
                relative
                h-[181px]
                flex-1
                min-w-0
                ${className}
            `}
        >

            {/* Title */}

            <h2
                className="
                    absolute
                    text-[16px]
                    font-bold
                "
                style={{
                    left: "13px",
                    top: "15px",
                }}
            >
                RECENT DETECTIONS
            </h2>

            {/* Table */}

            <div
                className="
                    absolute
                    rounded-[10px]
                    border
                    border-white
                    overflow-y-auto
                "
                style={{
                    left: "20px",
                    right: "20px",
                    top: "44px",
                    bottom: "10px",
                }}
            >

                <table
                    className="
                        w-full
                        table-fixed
                        text-[10px]
                    "
                >

                    <thead
                        className="
                            sticky
                            top-0
                            bg-[#101B30]
                        "
                    >
                        <tr className="h-[24px]">

                            <th className="font-normal text-left px-[8px]">
                                Time
                            </th>

                            <th className="font-normal text-left px-[8px]">
                                Packet
                            </th>

                            <th className="font-normal text-left px-[8px]">
                                Attack Type
                            </th>

                            <th className="font-normal text-left px-[8px]">
                                Confidence
                            </th>

                            <th className="font-normal text-left px-[8px]">
                                Latency
                            </th>

                        </tr>

                    </thead>

                    <tbody>

                        {detections.map((item, index) => (

                            <tr
                                key={index}
                                className="h-[20px]"
                            >

                                <td className="px-[8px] whitespace-nowrap">
                                    {item.timestamp.split(" ")[1]}

                                </td>

                                <td className="px-[8px] whitespace-nowrap">
                                    {item.packet_number}
                                </td>

                                <td
                                    className="px-[8px] whitespace-nowrap"
                                    style={{

                                        color:

                                            CLASS_INFO[item.prediction].color,

                                    }}
                                >

                                    {CLASS_INFO[item.prediction].displayName}

                                </td>

                                <td className="px-[8px] whitespace-nowrap">
                                    {item.confidence.toFixed(2)}%
                                </td>

                                <td className="px-[8px] whitespace-nowrap">
                                    {item.average_latency_ms.toFixed(2)} ms
                                </td>

                            </tr>

                        ))}

                    </tbody>

                </table>

            </div>

        </Panel>

    );

}

export default RecentDetectionSection;