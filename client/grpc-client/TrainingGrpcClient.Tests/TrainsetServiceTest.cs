using GrpcAcronymsClient;
using Microsoft.Extensions.Configuration;

namespace TrainingGrpcClient.Tests;

public class TrainsetServiceTest
{
    private readonly TrainsetServiceService _service;

    public TrainsetServiceTest()
    {
        var builder = new ConfigurationBuilder()
               .SetBasePath(Directory.GetCurrentDirectory())
               .AddJsonFile("appsettings.test.json", optional: true, reloadOnChange: true);

        var configuration = builder.Build();

        var grpcUrl = configuration.GetSection("GrpcSettings:ServerUrl").Value;

        _service = new TrainsetServiceService(grpcUrl);
    }

    public Trainset GetCreateDto()
    {
        var dto = new Trainset
        {
            Description = "start descripton"
        };

        return dto;
    }

    public Trainset GetUpdateDto(Trainset dto)
    {
        dto.Description = "updated escription";
        return dto;
    }


    [Fact]
    public async Task Create()
    {

        // Arrange
        var createDto = GetCreateDto();
        var tasks = new List<Task<Trainset>>();

        // Act
        for (int i = 0; i < 10; i++)
        {
            tasks.Add(_service.Create(createDto));
        }

        var results = await Task.WhenAll(tasks);

        // Assert
        foreach (var result in results)
        {
            Assert.NotNull(result);
            Assert.NotNull(result.CreateDt);
            Assert.NotNull(result.Id);
            Assert.Equal(createDto.Description, result.Description);
        }

    }

    [Fact]
    public async Task GetAll()
    {
        // Arrange

        // Act
        var result = await _service.GetAll();

        // Assert
        Assert.NotNull(result.List);

    }

    [Fact]
    public async Task GetById()
    {
        // Arrange
        Trainset dto = null;
        var result = await _service.GetAll();
        if (result.List.Count < 1)
        {
            var createDto = GetCreateDto();
            dto = await _service.Create(createDto);
        }
        else
        {
            dto = result.List[result.List.Count - 1];
        }

        // Act
        Trainset dtoByid = await _service.GetById(dto.Id);
        Assert.NotNull(dtoByid);
        Assert.Equal(dto.Id, dtoByid.Id);

    }

    [Fact]
    public async Task Update()
    {
        // Arrange
        Trainset dto = null;
        var result = await _service.GetAll();
        if (result.List.Count < 1)
        {
            var createDto = GetCreateDto();
            dto = await _service.Create(createDto);
        }
        else
        {
            dto = result.List[result.List.Count - 1];
        }

        var updateDto = GetUpdateDto(dto);

        // Act
        var updated = await _service.Update(updateDto);

        // Assert
        Assert.Equal(updateDto.Id, updated.Id);
        Assert.Equal(updateDto.Description, updated.Description);

    }

    [Fact]
    public async Task Delete()
    {

        // Arrange
        Trainset dto = null;
        
        var createDto = GetCreateDto();
        dto = await _service.Create(createDto);

        // Act
        await _service.Delete(dto);

        var res = await _service.GetAll();

        foreach (var item in res.List)
        {
            Assert.NotEqual(dto.Id, item.Id);
        }

    }
}
