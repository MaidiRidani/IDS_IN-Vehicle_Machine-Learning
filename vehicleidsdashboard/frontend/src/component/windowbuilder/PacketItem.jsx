function PacketItem({
    packetNumber,
    selected = false,
    configured = false,
    onClick,
}) {
    return (

        <div
            className="
                flex
                items-center
                h-[18px]
                cursor-pointer
            "
            onClick={onClick}
        >

            {/* Selector */}

            <div
                className="border border-white"
                style={{
                    width: "11px",
                    height: "11px",
                    backgroundColor:
                        selected
                            ? "#FF1A1A"
                            : configured
                                ? "#00D26A"
                                : "#FFFFFF",
                }}
            />

            {/* Packet */}

            <span
                className="
                    ml-[8px]
                    text-[14px]
                    font-bold
                    whitespace-nowrap
                "
            >
                Packet #{packetNumber}
            </span>

        </div>

    );
}

export default PacketItem;