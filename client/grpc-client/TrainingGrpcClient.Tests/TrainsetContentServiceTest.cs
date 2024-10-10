using GrpcAcronymsClient;

namespace TrainingGrpcClient.Tests;

public class TrainsetContentServiceTest
{
    private readonly TrainsetContentServiceService _service;

    public TrainsetContentServiceTest()
    {
        _service = new TrainsetContentServiceService();
    }
    public TrainsetContent GetCreateDto()
    {
        var dto = new TrainsetContent
        {
            Role = "user"
        };

        return dto;
    }

    public TrainsetContent GetUpdateDto(TrainsetContent dto)
    {
        dto.TraindataId = 2;
        return dto;
    }

    [Fact]
    public async Task Create()
    {
        // Arrange
        var dto = GetCreateDto();

        // Act
        var created = await _service.Create(dto);

        // Assert
        Assert.NotNull(created);
        Assert.NotNull(created.Id);
        Assert.Equal("user", created.Role);
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
        TrainsetContent dto = null;
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
        var dtoByid = await _service.GetById(dto.Id);
        Assert.NotNull(dtoByid);
        Assert.Equal(dto.Id, dtoByid.Id);

    }

    [Fact]
    public async Task Update()
    {
        // Arrange
        TrainsetContent dto = null;
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


        // Assert
        Assert.Equal(dto.TraindataId, updateDto.TraindataId);

    }

    [Fact]
    public async Task Delete()
    {

        // Arrange
        TrainsetContent dto = null;
        
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
