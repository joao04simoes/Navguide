export function NextHeading(atualPosition, NextPosition) {
    let NextHeading = 0
    if (atualPosition[0] === NextPosition[0] && atualPosition[1] > NextPosition[1])
        NextHeading = 3
    else if (atualPosition[0] === NextPosition[0] && atualPosition[1] < NextPosition[1])
        NextHeading = 1
    else if (atualPosition[0] > NextPosition[0] && atualPosition[1] === NextPosition[1])
        NextHeading = 4
    else if (atualPosition[0] < NextPosition[0] && atualPosition[1] === NextPosition[1])
        NextHeading = 2
    return NextHeading
}

export function GiveDirection(atualHeading, NextHeading, lastDirection) {
    const diff = atualHeading - NextHeading
    let direction = ""
    if (atualHeading === NextHeading)
        direction = "seguir em frente"
    else if (Math.abs(diff) === 2)
        direction = "virar para trás"
    else if (diff === 1 || diff === -3)
        direction = "virar para a esquerda"
    else if (diff === -1 || diff === 3)
        direction = "virar para a direita"
    else
        return "error"
    if (lastDirection === direction)
        return [direction, 0]
    else
        return [direction, 1]

}
