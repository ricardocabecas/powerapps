// Motor de testes: avalia fórmulas Power Fx com o interpretador open source da Microsoft
// (pacote NuGet Microsoft.PowerFx.Interpreter) e devolve os resultados em JSON.
//
// Utilização: dotnet run -- <entrada.json> <saida.json>
//
// Cada tarefa da entrada tem:
//   id       identificador do caso
//   modo     "avaliar" (analisa e calcula) ou "analisar" (só verifica a sintaxe)
//   cultura  "invariante" (formato dos ficheiros .pa.yaml) ou "pt-PT" (formato da barra de fórmulas)
//   vars     lista de {nome, expr}: variáveis de contexto (coleções, controlos simulados)
//   expr     fórmula a avaliar
//
// Diferenças conhecidas em relação ao Power Apps Studio (tratadas aqui):
//   * o interpretador não aceita o marcador de idioma "[$-en-US]" nos formatos de Text;
//     é removido antes da avaliação (no interpretador o formato já é lido em invariante).
//   * os números são tratados como Float (vírgula flutuante binária), como nas canvas apps.
using System.Globalization;
using System.Text.Json;
using System.Text.Json.Nodes;
using Microsoft.PowerFx;
using Microsoft.PowerFx.Types;

var entrada = JsonNode.Parse(File.ReadAllText(args[0])).AsArray();
var saida = new JsonArray();

foreach (var tarefa in entrada)
{
    var id = (string)tarefa["id"];
    var modo = (string)tarefa["modo"] ?? "avaliar";
    var cultura = (string)tarefa["cultura"] ?? "invariante";
    var expr = Preparar((string)tarefa["expr"]);
    var res = new JsonObject { ["id"] = id };
    try
    {
        var config = new PowerFxConfig(Features.PowerFxV1);
        config.EnableSetFunction();
        config.SymbolTable.EnableMutationFunctions();
        var motor = new RecalcEngine(config);
        var optInv = Opcoes(CultureInfo.InvariantCulture);
        var opt = cultura == "pt-PT" ? Opcoes(new CultureInfo("pt-PT")) : optInv;

        if (tarefa["vars"] is JsonArray vars)
        {
            foreach (var v in vars)
            {
                var nome = (string)v["nome"];
                var valor = await motor.EvalAsync(Preparar((string)v["expr"]), CancellationToken.None, optInv);
                if (valor is ErrorValue ev)
                    throw new Exception($"Erro ao preparar a variável {nome}: " + string.Join(" | ", ev.Errors.Select(e => e.Message)));
                motor.UpdateVariable(nome, valor);
            }
        }

        if (modo == "analisar")
        {
            var pr = motor.Parse(expr, opt);
            res["ok"] = pr.IsSuccess;
            if (!pr.IsSuccess) res["erro"] = string.Join(" | ", pr.Errors.Select(e => e.ToString()));
        }
        else
        {
            var valor = await motor.EvalAsync(expr, CancellationToken.None, opt);
            if (valor is ErrorValue ev)
            {
                res["ok"] = false;
                res["erro"] = string.Join(" | ", ev.Errors.Select(e => e.Message));
            }
            else
            {
                res["ok"] = true;
                res["valor"] = ParaJson(valor);
            }
        }
    }
    catch (Exception ex)
    {
        res["ok"] = false;
        res["erro"] = ex.Message;
    }
    saida.Add(res);
}

File.WriteAllText(args[1], saida.ToJsonString(new JsonSerializerOptions { WriteIndented = true }));
Console.WriteLine($"{saida.Count} tarefas processadas.");

static ParserOptions Opcoes(CultureInfo c) =>
    new ParserOptions { AllowsSideEffects = true, NumberIsFloat = true, Culture = c };

static string Preparar(string f) => f?.Replace("[$-en-US]", "");

static JsonNode ParaJson(FormulaValue v) => v switch
{
    BlankValue => null,
    NumberValue n => double.IsFinite(n.Value) ? JsonValue.Create(n.Value) : JsonValue.Create(n.Value.ToString(CultureInfo.InvariantCulture)),
    DecimalValue d => JsonValue.Create((double)d.Value),
    StringValue s => JsonValue.Create(s.Value),
    BooleanValue b => JsonValue.Create(b.Value),
    RecordValue r => ParaJsonRegisto(r),
    TableValue t => new JsonArray(t.Rows.Select(l => l.IsValue ? ParaJsonRegisto(l.Value)
                                    : (JsonNode)new JsonObject { ["__erro"] = string.Join(" | ", l.Error.Errors.Select(e => e.Message)) }).ToArray()),
    ErrorValue e => new JsonObject { ["__erro"] = string.Join(" | ", e.Errors.Select(x => x.Message)) },
    _ => JsonValue.Create(v.ToExpression())
};

static JsonObject ParaJsonRegisto(RecordValue r)
{
    var o = new JsonObject();
    foreach (var c in r.Fields) o[c.Name] = ParaJson(c.Value);
    return o;
}
