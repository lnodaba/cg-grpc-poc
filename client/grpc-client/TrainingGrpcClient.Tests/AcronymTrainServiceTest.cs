using GrpcAcronymsClient;



namespace TrainingGrpcClient.Tests;
public class AcronymTrainDataServiceTest
{
    private readonly AcronymTrainDataServiceService _service;

    public AcronymTrainDataServiceTest()
    {
        _service = new AcronymTrainDataServiceService();
    }

    public AcronymTrainData GetCreateDto()
    {
        var dto = new AcronymTrainData
        {
            ProvidedBy = "User",
            TextEn = "TermEn",
            TextFr = "TermFr",
            Reason = "Some reason",
        };

        return dto;
    }

    public AcronymTrainData GetUpdateDto(AcronymTrainData dto)
    {
        dto.TextEn = "UpdatedTermEn";
        dto.TextFr = "UpdatedTermFr";
        return dto;
    }

    [Fact]
    public async Task Create()
    {
        // Arrange
        var createDto = GetCreateDto();
        var tasks = new List<Task<AcronymTrainData>>();

        // Act
        for (int i = 0; i < 10; i++)
        {
            tasks.Add(_service.Create(createDto));
        }

        var results = await Task.WhenAll(tasks);
        
        foreach (var result in results)
        {
            // Assert
            Assert.NotNull(result);
            Assert.NotNull(result.Id);
            Assert.NotEqual(createDto.Id, result.Id);
            Assert.NotEqual(0, result.Id);
            Assert.Equal(createDto.TextEn, result.TextEn);
            Assert.Equal(createDto.TextFr, result.TextFr);
            Assert.NotNull(result.CreateDt);
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
        AcronymTrainData dto = null;
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
        AcronymTrainData dtoByid = await _service.GetById(dto.Id);
        Assert.NotNull(dtoByid);
        Assert.Equal(dto.Id, dtoByid.Id);

    }

    [Fact]
    public async Task Update()
    {
        // Arrange 
        AcronymTrainData dto = null;
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
        Assert.Equal(dto.Id, updateDto.Id);
        Assert.Equal(updateDto.TextEn, updated.TextEn);
        Assert.Equal(updateDto.TextFr, updated.TextFr);
        Assert.Equal(updateDto.Reason, updated.Reason);
    }

    [Fact]
    public async Task Delete()
    {

        // Arrange
        AcronymTrainData dto = null;
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
        await _service.Delete(dto);

        var res = await _service.GetAll();

        foreach (var item in res.List)
        {
            Assert.NotEqual(dto.Id, item.Id);
        }

    }
}


