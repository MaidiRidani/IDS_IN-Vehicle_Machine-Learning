import Panel from "../common/Panel";
import PacketItem from "./PacketItem";

function AvailablePacketSection({

    packets,

    packetPage,

    setPacketPage,

    selectedPacket,

    setSelectedPacket,

    configurations,

}) {
    console.log(selectedPacket);

    const firstPacket =
        packets.length > 0
            ? packets[0]
            : "-";

    const lastPacket =
        packets.length > 0
            ? packets[packets.length - 1]
            : "-";

    return (

        <Panel
            className="
                relative
                w-[280px]
                h-[345px]
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
                    top: "11px",
                }}
            >
                AVAILABLE PACKET
            </h2>

            {/* List */}

            <div
                className="
                    absolute
                    w-[255px]
                    h-[250px]
                    rounded-[10px]
                    overflow-y-auto
                    overflow-x-hidden
                    bg-[#05070D]
                "
                style={{
                    left: "0px",
                    bottom: "45px",
                }}
            >

                <div
                    className="flex flex-col"
                    style={{
                        marginLeft: "8px",
                        marginTop: "8px",
                        rowGap: "7px",
                    }}
                >

                    {packets.map(packetNumber => {

                        const isConfigured = configurations.some(
                            config => config.packetNumber === packetNumber
                        );

                        return (

                            <PacketItem
                                key={packetNumber}
                                packetNumber={packetNumber}
                                selected={selectedPacket === packetNumber}
                                configured={isConfigured}
                                onClick={() => setSelectedPacket(packetNumber)}
                            />

                        );

                    })}
                </div>

            </div>
            <div
                className="
                    absolute
                    bottom-[8px]
                    left-0
                    w-full
                    flex
                    items-center
                    justify-center
                    gap-[10px]
                "
            >

                <button
                    type="button"
                    className="
                        w-[55px]
                        h-[22px]
                        rounded
                        border
                        border-white
                        text-[10px]
                    "
                    disabled={packetPage === 0}
                    onClick={() =>
                        setPacketPage(prev => Math.max(0, prev - 1))
                    }
                >
                    Prev
                </button>

                <div
                    className="
                        flex
                        flex-col
                        items-center
                    "
                >

                    <span className="text-[10px]">
                        Page {packetPage + 1}
                    </span>

                    <span className="text-[9px]">
                        Packet {firstPacket}–{lastPacket}
                    </span>

                </div>

                <button
                    type="button"
                    className="
                        w-[55px]
                        h-[22px]
                        rounded
                        border
                        border-white
                        text-[10px]
                    "
                    disabled={packets.length < 500}
                    onClick={() =>
                        setPacketPage(prev => prev + 1)
                    }
                >
                    Next
                </button>
            </div>

        </Panel>

    );
}

export default AvailablePacketSection;