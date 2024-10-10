using GrpcAcronymsClient;

namespace TrainingGrpcClient.Tests;

public class TrainsetServiceTest
{
    private readonly TrainsetServiceService _service;

    public TrainsetServiceTest()
    {
        _service = new TrainsetServiceService();
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
        return dto;
    }


    [Fact]
    public async Task Create()
    {
        // Arrange
        var acronym = new Trainset
        {
            Description= "start descripton"
        };

        // Act
        var created = await _service.Create(acronym);

        // Assert
        Assert.NotNull(created);
        Assert.NotNull(created.CreateDt);
        Assert.NotNull(created.Id);

        Assert.Equal(acronym.Description, created.Description);

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
        var result = await _service.GetAll();
        if (result.List.Count < 1)
        {
            await Create();
        }
        var last = result.List[result.List.Count - 1];

        // Act
        var updated = await _service.Update(last);

        // Assert
        

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
