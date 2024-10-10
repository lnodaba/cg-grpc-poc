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

        try
        {
            Parallel.For(0, 10,async (i) => await _service.Create(createDto) );
            Thread.Sleep(3000);
        }
        catch (Exception ex)
        {
            throw;
        }
        // Act

        // Assert
      
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
        Assert.Equal(updateDto.TextEn, updated.TextEn);
        Assert.Equal(updateDto.TextFr, updated.TextFr);
        Assert.NotEqual(updateDto.UpdateDt, updated.UpdateDt);
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


