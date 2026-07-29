import Panel from "./Panel";

function ConfigurationLockedDialog({

    show,

    onClose,

}) {

    if (!show) {

        return null;

    }

    return (

        <div
            className="
                fixed
                inset-0
                flex
                items-center
                justify-center
                bg-black/50
                z-[999]
            "
        >

            <Panel
                className="
                    w-[340px]
                    h-[180px]
                    flex
                    flex-col
                    items-center
                "
            >

                <h2
                    className="
                        mt-[18px]
                        text-[22px]
                        font-bold
                    "
                >
                    Configuration Locked
                </h2>

                <p
                    className="
                        mt-[18px]
                        w-[280px]
                        text-center
                        text-[14px]
                    "
                >
                    Packet configurations already exist.
                    <br />
                    Clear all packet configurations before changing
                    the model or preprocessing configuration.
                </p>

                <button
                    className="
                        mt-[22px]
                        w-[110px]
                        h-[36px]
                        useState(20);-full
                        bg-green-700
                        font-bold
                    "
                    onClick={onClose}
                >
                    OK
                </button>

            </Panel>

        </div>

    );

}

export default ConfigurationLockedDialog;