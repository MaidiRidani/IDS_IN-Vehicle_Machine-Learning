const WINDOWS = [32, 64, 128, 256];

const LEVELS = [1, 2, 3, 4];

export function getValidConfigurations(inputSize) {

    const result = [];

    for (const windowSize of WINDOWS) {

        for (const level of LEVELS) {

            const outputSize = windowSize / (2 ** level);

            if (outputSize === inputSize) {

                result.push({

                    windowSize,

                    level,

                });

            }

        }

    }

    return result;

}