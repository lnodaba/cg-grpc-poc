

using grpc_client.services;
using GrpcAcronymsClient;

var service = new grpc_client.services.AcronymServiceService();

// Create Acronym
Acronym acronym = new Acronym
{
    Id = 23,
    TextEn = "TermEn",
    TextFr = "TermFr",
    AcronymEn = "acronym_en",
    AcronymFr = "AcronymFr"
};

// Testing create method
Console.WriteLine("Creating acronym...");
var createdAcronym = await service.create(acronym);
Console.WriteLine("Acronym created: ");
Console.WriteLine($"ID: {createdAcronym.Id}, TextEn: {createdAcronym.TextEn}, TextFr: {createdAcronym.TextFr}");

// Testing get_all method
Console.WriteLine("Fetching all acronyms...");
var res = await service.get_all();
Console.WriteLine("Response to get_all:");
foreach (var item in res.List)
{
    Console.WriteLine($"ID: {item.Id}, AcronymEn: {item.AcronymEn}, AcronymFr: {item.AcronymFr}, TextEn: {item.TextEn}, TextFr: {item.TextFr}, CreateDt: {item.CreateDt}, UpdateDt: {item.UpdateDt}");
}

// Testing update method
Acronym updatedAcronym = new Acronym
{
    Id = createdAcronym.Id, // Use the created acronym ID for update
    TextEn = "UpdatedTermEn",
    TextFr = "UpdatedTermFr",
    AcronymEn = "updated_acronym_en",
    AcronymFr = "updated_AcronymFr"
};

Console.WriteLine("Updating acronym...");
var updated = await service.update(updatedAcronym);
Console.WriteLine("Acronym updated: ");
Console.WriteLine($"ID: {updated.Id}, TextEn: {updated.TextEn}, TextFr: {updated.TextFr}");

// Testing delete method
Console.WriteLine("Deleting acronym...");
var deleteResponse = await service.delete(updatedAcronym);
Console.WriteLine("Acronym deleted successfully.");

Console.WriteLine("All gRPC operations tested successfully!");