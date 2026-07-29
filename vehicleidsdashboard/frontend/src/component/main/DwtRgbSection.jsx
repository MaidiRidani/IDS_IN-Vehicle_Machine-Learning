import Panel from "../common/Panel";
import { getPreprocessedImageUrl } from "../../api/preprocessing";
import { useState } from "react";


function DwtRgbSection({

    preprocessedImages,

    className = "",

}) {
    const [selectedImage, setSelectedImage] = useState(null);
    const [searchPacket, setSearchPacket] = useState("");
    const hasImage = preprocessedImages.length > 0;
    const filteredImages =

        preprocessedImages.filter(image =>

            searchPacket === ""

                ||

            image.packet_number
                .toString()
                .includes(searchPacket)

        );
    const imageUrl = hasImage

        ? getPreprocessedImageUrl(0)

        : null;
    function getBorderColor(label) {

        switch (label) {

            case "Normal":
                return "border-green-500";

            case "C_D":
                return "border-red-500";

            case "C_R":
                return "border-blue-500";

            case "F_I":
                return "border-yellow-400";

            case "M_F":
                return "border-purple-500";

            case "P_I":
                return "border-gray-500";

            default:
                return "border-white";

        }

    }
    return (
        <Panel
            className={`
                relative
                flex-1
                h-[277px]
                flex
                flex-col
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
                    left: "20px",
                    top: "13px",
                }}
            >
                DWT RGB INPUT
            </h2>
            <input

                type="text"

                placeholder="Search Packet..."

                value={searchPacket}

                onChange={(e) =>

                    setSearchPacket(e.target.value)

                }

                className="
                    absolute
                    h-[24px]
                    w-[30%]
                    min-w-[130px]
                    max-w-[180px]
                    right-[18px]
                    top-[12px]
                    rounded
                    border
                    border-[#334155]
                    bg-[#101B30]
                    px-[8px]
                    text-[10px]
                    outline-none
                "

            />

            {/* ================= DWT Preview ================= */}

            <div
                className="
                    absolute
                    h-[180px]
                    rounded-[10px]
                    border
                    border-white
                    overflow-hidden
                    "
                    style={{
                        left:12,
                        right:12,
                        top:42,
                    }}
            >
                {
                    preprocessedImages.length === 0 ? (

                        <div
                            className="
                                w-full
                                h-full
                                flex
                                items-center
                                justify-center
                                text-[12px]
                                text-white/60
                            "
                        >
                            No preprocessing image.
                        </div>

                    ) : (

                        <div
                            className="
                                w-full
                                h-full
                                overflow-y-auto
                                p-[8px]
                            "
                        >

                            <div
                                className="
                                    grid
                                    grid-cols-4
                                    gap-[6px]
                                "
                                style={{
                                    gridTemplateColumns:
                                        "repeat(auto-fill,minmax(85px,1fr))",
                                }}
                            >

                                {filteredImages.map((image, index) => (

                                    <img
                                        onClick={() => setSelectedImage(image)}

                                        key={index}

                                        src={getPreprocessedImageUrl(index)}

                                        alt={`RGB ${index}`}

                                        title={
                `Packet #${image.packet_number}
                Selected : ${image.selected_label}
                Window : ${image.window_label}
                Position : ${image.position}`
                                        }

                                        className={`
                                            w-full
                                            aspect-square
                                            object-contain
                                            border-2
                                            rounded
                                            cursor-pointer
                                            transition
                                            duration-150
                                            hover:scale-105
                                            hover:shadow-lg
                                            ${getBorderColor(image.window_label)}
                                        `}

                                    />

                                ))}

                            </div>

                        </div>

                    )
                }

            </div>
            {/* ================= IMAGE SIZE ================= */}

            <div
                className="absolute flex items-center"
                style={{
                    left: "32px",
                    top: "239px",
                }}
            >

                <p
                    className="
                        text-[10px]
                        font-normal
                        mr-[7px]
                    "
                >
                    Image Size
                </p>

                <div
                    className="
                        w-[78px]
                        h-[26px]
                        rounded-full
                        border
                        border-white
                        flex
                        items-center
                        justify-center
                    "
                >
                    <span className="text-[10px]">
                        {
                            hasImage

                                ? `${preprocessedImages[0].shape[1]} × ${preprocessedImages[0].shape[0]}`

                                : "-"
                        }
                                            </span>
                </div>

            </div>

            {/* ================= FILTER ================= */}


            {/* ================= FILTER ================= */}

            <div
                className="absolute flex items-center"
                style={{
                    left: "198px",
                    top: "239px",
                }}
            >

                <p
                    className="
                        text-[10px]
                        font-normal
                        mr-[6px]
                    "
                >
                    Filter
                </p>

                <div
                    className="
                        w-[60px]
                        h-[26px]
                        rounded-full
                        border
                        border-white
                        flex
                        items-center
                        justify-center
                        text-[10px]
                    "
                >
                    Coiflet 1
                </div>

                <div
                    className="
                        ml-[3px]
                        w-[42px]
                        h-[26px]
                        rounded-full
                        border
                        border-white
                        flex
                        items-center
                        justify-center
                        text-[10px]
                    "
                >
                    DB 3
                </div>

                <div
                    className="
                        ml-[3px]
                        w-[56px]
                        h-[26px]
                        rounded-full
                        border
                        border-white
                        flex
                        items-center
                        justify-center
                        text-[10px]
                    "
                >
                    Rbio 1.3
                </div>

            </div>
            {
                selectedImage && (

                    <div
                        className="
                            fixed
                            inset-0
                            bg-black/70
                            flex
                            items-center
                            justify-center
                            z-[9999]
                        "
                        onClick={() => setSelectedImage(null)}
                    >

                        <div
                            className="
                                bg-[#101B30]
                                border
                                border-white
                                rounded-[12px]
                                p-[12px]
                            "
                            onClick={(e) => e.stopPropagation()}
                        >

                            <img

                                src={
                                    getPreprocessedImageUrl(
                                        preprocessedImages.findIndex(
                                            img =>

                                                img.packet_number ===
                                                selectedImage.packet_number
                                        )
                                    )
                                }

                                alt="Preview"

                                className="
                                    w-[420px]
                                    h-[420px]
                                    object-contain
                                    rounded
                                    border
                                    border-[#334155]
                                "

                            />

                            <div className="mt-[10px] text-[11px]">

                                <p>

                                    <b>Packet :</b>

                                    {selectedImage.packet_number}

                                </p>

                                <p>

                                    <b>Label :</b>

                                    {selectedImage.window_label}

                                </p>

                                <p>

                                    <b>Selected :</b>

                                    {selectedImage.selected_label}

                                </p>

                                <p>

                                    <b>Position :</b>

                                    {selectedImage.position}

                                </p>

                            </div>

                        </div>

                    </div>

                )
            }

        </Panel>
    );
}

export default DwtRgbSection;