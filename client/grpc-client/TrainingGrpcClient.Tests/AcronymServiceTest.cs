using System;
using System.Collections.Generic;
using GrpcAcronymsClient;


namespace TrainingGrpcClient.Tests;

public class AcronymServiceTest
{
    private readonly AcronymServiceService _service;

    public AcronymServiceTest()
    {
        _service = new AcronymServiceService();
    }

    public Acronym GetCreateDto()
    {
        var dto = new Acronym
        {
            TextEn = "TermEn",
            TextFr = "TermFr",
            AcronymEn = "acronymEn",
            AcronymFr = "AcronymFr"
        };

        return dto;
    }

    public Acronym GetUpdateDto(Acronym dto)
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
        var tasks = new List<Task<Acronym>>();

        // Act
        for (int i = 0; i < 10; i++)
        {
            tasks.Add(_service.Create(createDto));
        }

        var results = await Task.WhenAll(tasks);

        // Assert
        foreach (var result in results)
        {
            Assert.NotNull(result); // Check if the result is not null
            Assert.NotEqual(0, result.Id); // Check that the created object's Id is not zero
            Assert.Equal(createDto.AcronymEn, result.AcronymEn); // Check if AcronymEn matches
            Assert.Equal(createDto.AcronymFr, result.AcronymFr); // Check if AcronymFr matches
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
        Acronym dto = null;
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
        Acronym dtoByid = await _service.GetById(dto.Id);
        Assert.NotNull(dtoByid);
        Assert.Equal(dto.Id, dtoByid.Id);

    }



    [Fact]
    public async Task Update()
    {
        // Arrange
        Acronym dto = null;
        var result = await _service.GetAll();
        if (result.List.Count < 1)
        {
            var createDto = GetCreateDto();
            dto = await _service.Create(createDto);

        } else
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
        Assert.NotNull(updated.UpdateDt);
    }

    [Fact]
    public async Task Delete()
    {

        // Arrange
        Acronym dto = null;

        var result = await _service.GetAll();
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


