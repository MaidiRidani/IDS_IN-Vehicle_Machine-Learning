import Panel from "../common/Panel";
import { CLASS_INFO } from "../../constants/classInfo";



function RecentDetectionSection({

    history,

}) {

    const detections =

        [...(history ?? [])]

            .reverse()

    return (

        <Panel
            className="
                relative
                w-[476px]
                h-[181px]
            "
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
                    w-[436px]
                    h-[127px]
                    rounded-[10px]
                    border
                    border-white
                    overflow-y-auto
                "
                style={{
                    left: "20px",
                    top: "44px",
                }}
            >

                <table className="w-full text-[10px]">

                    <thead
                        className="
                            sticky
                            top-0
                            bg-[#101B30]
                        "
                    >
                        <tr className="h-[24px]">

                            <th className="font-normal text-left pl-[10px]">
                                Time
                            </th>

                            <th className="font-normal text-left">
                                Packet
                            </th>

                            <th className="font-normal text-left">
                                Attack Type
                            </th>

                            <th className="font-normal text-left">
                                Confidence
                            </th>

                            <th className="font-normal text-left">
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

                                <td className="pl-[10px]">
                                    {item.timestamp.split(" ")[1]}

                                </td>

                                <td>
                                    {item.packet_number}
                                </td>

                                <td
                                    style={{

                                        color:

                                            CLASS_INFO[item.prediction].color,

                                    }}
                                >

                                    {CLASS_INFO[item.prediction].displayName}

                                </td>

                                <td>
                                    {item.confidence}
                                </td>

                                <td>
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